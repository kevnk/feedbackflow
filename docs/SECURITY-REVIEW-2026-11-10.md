# Security review: feedbackflow (Nov 10, 2026)

## Bottom line

- **The native host could write or empty any file the user owns.** Branch `overflow/native-host-path` fixes it: the host now writes only `~/.feedbackflow/feedback.log`.
- **A web page could not use that hole today.** The extension always sends a fixed path, and only this extension's ID may call the host. The fix is defense-in-depth: it stops one extension change from turning into "any page can append to `~/.zshrc`."
- **The bigger open problem: any website can write into the AI's feedback log.** The extension runs on every site, so any page you visit can plant text that your coding assistant later reads as "user feedback." That is prompt injection into a coding agent. It is must-fix, but the fix changes who can send feedback, so it goes in its own PR (`overflow/feedback-origin-allowlist`).
- **Five nice-to-fix items** are listed below and not changed.

## Scope and method

- Fresh clone of `kevnk/feedbackflow` at `main` = `a1fb6c0`.
- I read the whole path a piece of feedback takes:
  - page → `chrome-extension/feedbackflow-api.js` → `content.js` → `background.js`;
  - → native host `native-host/feedbackflow_host.py` → `~/.feedbackflow/feedback.log`;
  - → readers: `mcp/mcp_server.py`, `scripts/add_feedback_to_composer.py` and `scripts/watch_and_add_feedback.py`.
- I also read the installers (`native-host/install_host.py`, `scripts/update_extension_id.py`, `setup.py`, `cli/install_ff_globally.py`) and the VS Code extension (`extension.js`).
- Line numbers are from `a1fb6c0`.

## Must-fix

### 1. The native host writes or empties any file (fixed)

- **Where:**
  - `native-host/feedbackflow_host.py:51-58`: `writeFeedback` appended `content` to `os.path.join(home_dir, message['path'])`.
  - `:64-68`: `clearFeedback` emptied that path the same way.
- **How it breaks:** an absolute `path` replaces the home folder entirely (`os.path.join` drops everything before it), and `../` climbs out of it. A `path` of `.zshrc` writes to a shell startup file.
- **Who can reach it:**
  - Only an extension listed in the host's `allowed_origins` (`com.feedbackflow.host.json.example:6-8`, written by `install_host.py:35-36` and `update_extension_id.py:35`).
  - The extension always sends `.feedbackflow/feedback.log` (`background.js:3`, `:38`, `:78`). So a page cannot choose the path today.
- **Fix:**
  - The host ignores `path` and always writes `~/.feedbackflow/feedback.log`.
  - `background.js` no longer sends a `path`.
- **Tests:** `native-host/test_feedbackflow_host.py`.
  - They run the real host as Chrome does (framed JSON on stdin), with `HOME` set to a temp folder.
  - 4 of the 5 failed before the fix: `../`, absolute path, `.zshrc` write, and `.zshrc` clear.

### 2. Any website can write into the AI's feedback log (open, separate PR)

- **Where:**
  - The content script runs on every site (`chrome-extension/manifest.json:19-24`), and `feedbackflow-api.js` is exposed to every site (`:25-30`). So every page gets `window.FeedbackFlow.sendFeedback`.
  - `content.js:35-66` (postMessage) and `:69-96` (custom event) forward any page's text to `background.js:10-66`. That code appends it to `feedback.log` through the host.
- **Who reads the log:**
  - The MCP server serves it to the assistant: resource `feedback://log`, and the prompt `analyze_feedback` (`mcp/mcp_server.py`).
  - `scripts/add_feedback_to_composer.py:213-227` copies it to the clipboard to paste into Cursor's composer.
  - The README sells exactly this loop: "feedback collection, AI analysis, and code improvement."
- **Impact:**
  - Any site you visit while the extension is on can plant instructions that your coding agent reads as feedback from your own site.
  - The page writes the `Feedback:` text, so it can also forge whole entries, with a fake separator line and a fake `URL: http://localhost:3000`.
  - There is no size limit (see #7), so a page can also fill the disk.
- **Fix, proposed in PR `overflow/feedback-origin-allowlist`:** `background.js` accepts feedback only from local development origins (`localhost`, `127.0.0.1`, `*.test`, `*.localhost`) and from sites the user allows. It also caps the entry size and stops forged separators.

## Nice-to-fix (not changed)

3. **Notification helpers build shell commands from strings.**
   - `scripts/add_feedback_to_composer.py:55-62` and `scripts/watch_and_add_feedback.py:56-61` run `os.system(f"osascript -e '... \"{message}\" ...'")`.
   - The Windows branch uses `subprocess.run(..., shell=True)` (`:78` in the watcher).
   - Today they are only called with fixed text (`add_feedback_to_composer.py:224-227`, `watch_and_add_feedback.py:225-228`), so feedback can't reach them. But one future call that passes feedback text would be a shell injection.
   - Fix: `subprocess.run(['osascript', '-e', script])` with the strings escaped for AppleScript.
4. **The VS Code command runs a script from whatever folder is open.**
   - `extension.js:19-22` runs `python "<workspace>/scripts/add_feedback_to_composer.py"` through `exec`.
   - With any repo open, the command runs that repo's copy of the script. A folder name containing `"` or `$(` also breaks out of the quotes.
   - `:46` and `:59` send a workspace path to a terminal the same way.
   - Fix: use `context.extensionPath` and `execFile`.
5. **Installers pass paths through a shell.** `setup.py:107` and `cli/install_ff_globally.py:65` run `sudo ln -sf {ff_path} /usr/local/bin/ff` with `shell=True`. A checkout path with a space or a quote breaks or misfires under `sudo`. Fix: an argument list.
6. **The MCP server's SSE mode probably doesn't start, and its bind address is unchecked.**
   - `mcp/mcp_server.py:308` calls `mcp.run(port=args.port)`. In the Python MCP SDK I know, `FastMCP.run()` takes a transport, not a port, and `port` and `host` are server settings.
   - Some older SDK releases also defaulted `host` to `0.0.0.0`. That would put the unauthenticated `add_feedback` and `clear_feedback` tools on the local network.
   - Not verified: the `mcp` package isn't installed here, and I didn't install it.
7. **The native host takes messages of any size.**
   - `feedbackflow_host.py:12-20` reads whatever length the 4-byte header announces, and Chrome lets an extension send a host messages many megabytes long.
   - Together with #2, a page can fill the disk.
   - Fix: refuse entries over a cap. The #2 PR caps entries in `background.js`, before they reach the host.

## How to check this branch

```bash
python3 -m unittest discover -s native-host   # 5 tests; HOME is a temp folder
node --check chrome-extension/background.js
```
