- [x] Is there a way to add the feedback.log to the context of composer easily in cursor/vscode?
- [x] Is there a way to clear the feedback.log? 
- [x] For sending feedback (in the popup and sample website), send feedback with command/crtl + enter; add the shortcut indication on the button 
- [x] if I run watch log in cursor, every time it updates, can we run "Add Feedback to Composer"? is those possible?
- [x] Error when trying to send feedback from console.
	```
	FeedbackFlow.sendFeedback("ok what's up")
	content.js:38 Uncaught Error: Extension context invalidated.
			at content.js:38:20
	(anonymous) @ content.js:38Understand this errorAI
	true
	```
- [x] instead of creating a copy of the feedback.log, can we just open the ~/.feedbackflow/feedback.log file in the editor?
- [x] is native-host/com.feedbackflow.host.json created when the extension is installed, if so, it probably should be in the repo. If not, we shouldn't use my username in the path.
  - Solution: Created com.feedbackflow.host.json.example with placeholder path, added the actual file to .gitignore, and updated install_host.py to use the example as a template.
- [x] Create some .cursorrules for the project and .github/copilot-instructions.md that can be copied into the user's .cursorrules and .github/copilot-instructions.md files — for all project if possible.
  - Solution: Created a separate `ff` command-line tool that can be used to add FeedbackFlow AI assistant integration files to any project.
  - Added multiple options for installing the `ff` command globally:
    1. Interactive option during setup.py execution
    2. Dedicated install_ff_globally.py script
    3. Manual installation instructions
  - Enhanced the `ff` command to intelligently merge with existing files:
    1. Merges with existing .cursorrules in both home directory and project directory
    2. Merges with existing .github/copilot-instructions.md in the project directory
- [x] Add MCP functionality to this project where it makes sense — reference https://github.com/modelcontextprotocol/python-sdk
- [ ] Refactor this project to make it easier to understand and maintain — add comments, improve variable names, etc.
	- NOTE: Think through carefully and use the best solution for this kind of project
		- if this were a distributed project, what would be the best way to structure it?
		- would it be better to have a single feedbackflow-<platform> repo for each platform, with the platform-specific files in platform-specific directories or keep it all in one repo since nothing will work without the others?
  - [ ] Move chrome extension files to a separate chrome-extension directory?
	- [ ] Move MCP files to a separate mcp directory?
	- [ ] Move scripts to a separate scripts directory maybe?
- [ ] In all the cli prompts can you make them (Y/n) instead (defaulting to y)?