# Feedback Flow Chrome Extension

A Chrome extension that allows you to send feedback from your website to your AI assistant. The feedback is stored in a log file that can be easily accessed by Cursor or VS Code.

## Features

- Send feedback directly from any website using the extension popup
- JavaScript API for websites to send feedback programmatically
- Native messaging host to write feedback to a local log file
- Python script to read and watch the feedback log
- VS Code/Cursor integration via tasks
- Easy addition of feedback log to Cursor composer context
- `ff` command-line tool for AI assistant integration
- Model Context Protocol (MCP) integration for direct AI assistant access to feedback

## Project Structure

The project is organized into the following directories:

- `chrome-extension/` - Chrome extension files (manifest, popup, content script, etc.)
- `native-host/` - Native messaging host for communication between Chrome and the local system
- `scripts/` - Utility scripts for reading feedback, adding to composer, etc.
- `mcp/` - Model Context Protocol integration for AI assistants
- `cli/` - Command-line tools for AI assistant integration
- `docs/` - Documentation files
- `sample-website/` - Sample website demonstrating the JavaScript API

## Installation

### Quick Setup

The easiest way to set up the extension is to use the provided setup script:

```bash
python setup.py
```

This will:
- Install required dependencies
- Create icon files for the extension
- Install the native messaging host
- Make the `ff` command executable
- Guide you through loading the extension in Chrome

Alternatively, you can use the VS Code/Cursor task "Setup Extension" to run the setup script.

### Manual Installation

#### 1. Install the Chrome Extension

1. Clone this repository or download it to your local machine
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable "Developer mode" in the top-right corner
4. Click "Load unpacked" and select the `chrome-extension` directory of this project
5. The Feedback Flow extension should now appear in your extensions list

#### 2. Install the Native Messaging Host

The native messaging host allows the extension to write to a log file on your system.

##### Automatic Installation

Run the installation script:

```bash
python native-host/install_host.py
```

This will:
- Install the native messaging host for Chrome
- Create the `.feedbackflow` directory in your home folder
- Create an empty `feedback.log` file

After installing the extension, you need to update the native messaging host with your extension ID:

```bash
python scripts/update_extension_id.py YOUR_EXTENSION_ID
```

Replace `YOUR_EXTENSION_ID` with the ID of your extension, which you can find in Chrome's extension management page (chrome://extensions/) after enabling Developer mode.

##### Troubleshooting

If the automatic installation doesn't work:

1. The repository contains an example manifest file (`native-host/com.feedbackflow.host.json.example`). During installation, this file is used as a template to create the actual manifest file with the correct paths.

2. If you need to manually set up the native host:
   - Copy the example manifest file to create `native-host/com.feedbackflow.host.json`
   - Replace `PLACEHOLDER_PATH` with the absolute path to the `native-host/feedbackflow_host.py` script
   - After loading the extension, update the allowed origins with your extension ID

3. Copy the manifest file to the appropriate location:
   - **macOS**: `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/`
   - **Linux**: `~/.config/google-chrome/NativeMessagingHosts/`
   - **Windows**: Add a registry key (see installation script for details)

4. Make the host script executable:
   ```bash
   chmod +x native-host/feedbackflow_host.py
   ```

## Usage

### Using the Extension Popup

1. Click on the Feedback Flow extension icon in your browser
2. Type your feedback in the text area
3. Click "Send Feedback"

### Using the JavaScript API in Your Website

The extension injects a JavaScript API into every web page. You can use it like this:

```javascript
// Check if the Feedback Flow API is available
if (window.FeedbackFlow) {
  // Send feedback to your AI assistant
  window.FeedbackFlow.sendFeedback("Your feedback message here");
}

// Listen for responses
window.addEventListener('message', function(event) {
  if (event.source !== window) return;
  
  if (event.data.type && event.data.type === 'FEEDBACK_FLOW_RESPONSE') {
    console.log('Feedback sent:', event.data.success);
  }
});
```

### Reading Feedback in VS Code/Cursor

The repository includes VS Code tasks for reading feedback:

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) to open the command palette
2. Type "Tasks: Run Task" and select it
3. Choose one of the following tasks:
   - "Read Feedback Log" - Displays the current contents of the log file
   - "Watch Feedback Log" - Continuously watches for new feedback entries
   - "Watch and Add Feedback to Composer" - Watches for new feedback and automatically adds it to the Cursor composer
   - "Add Feedback Log to Composer" - Copies the feedback log to the clipboard and opens it in the editor
   - "Clear Feedback Log" - Clears the feedback log file
   - "Install Native Host" - Runs the installation script
   - "Setup Extension" - Runs the complete setup script
   - "Run Sample Website" - Starts a local server for the sample website
   - "Check Extension Setup" - Verifies that the extension is set up correctly

## Sample Website

A sample website is included in the `sample-website` directory. You can run it using the VS Code/Cursor task "Run Sample Website", or manually with:

```bash
cd sample-website
python -m http.server 8000
```

Then open http://localhost:8000 in your browser to see a demonstration of how to use the Feedback Flow API.

## Troubleshooting

If the extension isn't working:

1. Run the check script to verify your setup:
   ```bash
   python check_extension.py
   ```
   
2. Check if the native messaging host is installed correctly
3. Look for errors in the Chrome extension's background page (inspect the extension)
4. Check the error log in the `.feedbackflow` directory in your home folder

### Native Messaging Issues

If you see a "Native messaging error" when sending feedback:

1. Make sure you've updated the extension ID in the native messaging host manifest:
   ```bash
   python scripts/update_extension_id.py YOUR_EXTENSION_ID
   ```
   Replace `YOUR_EXTENSION_ID` with the ID of your extension, which you can find in Chrome's extension management page (chrome://extensions/) after enabling Developer mode.

2. Check that the `nativeMessaging` permission is in the extension's manifest.json
3. Reload the extension after making any changes
4. Verify that the native messaging host script is executable:
   ```bash
   chmod +x native-host/feedbackflow_host.py
   ```

## Using Feedback with Cursor Composer

To easily add the feedback log to the Cursor composer context, you can use one of the following methods:

### Method 1: Use the VS Code Task

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) to open the Command Palette
2. Type "Tasks: Run Task" and select it
3. Select "Add Feedback Log to Composer"
4. The feedback log will be copied to your workspace, opened in the editor, and its content will be copied to your clipboard
5. You can now paste the content directly into the Composer

### Method 2: Run the Script or Shortcut File

#### On macOS:
Double-click the `Add Feedback to Composer.command` file or run:
```bash
./add_feedback.sh
```

#### On Windows:
Double-click the `add_feedback.bat` file or run:
```
add_feedback.bat
```

Or directly with Python on any platform:
```bash
python add_feedback_to_composer.py
```

This will:
1. Copy the feedback log to your workspace
2. Open it in the editor
3. Copy its content to your clipboard
4. Show a notification

You can then paste the content directly into the Composer, which is the easiest method to add it to the context.

## AI Assistant Integration

The FeedbackFlow extension includes a command-line tool called `ff` that helps AI assistants understand how to use FeedbackFlow in your projects.

### Using the `ff` Command

To add FeedbackFlow AI assistant integration to any project:

```bash
# Navigate to the FeedbackFlow directory
cd path/to/feedbackflow

# Run the ff command with your project directory
./ff ./path/to/your-project
```

#### Installing `ff` Globally

You have several options to make the `ff` command available globally:

##### Option 1: During Setup

When running `setup.py`, you'll be asked if you want to install the `ff` command globally. If you choose yes:
- On Windows: The FeedbackFlow directory will be added to your PATH
- On macOS/Linux: A symlink will be created in /usr/local/bin

##### Option 2: Using the Installation Script

Run the dedicated installation script:

```bash
python install_ff_globally.py
```

This will install the `ff` command globally on your system.

##### Option 3: Manual Installation

###### On Windows:
```
setx PATH "%PATH%;C:\path\to\feedbackflow"
```

###### On macOS/Linux:
```bash
# Add to PATH
echo 'export PATH="$PATH:/path/to/feedbackflow"' >> ~/.bashrc
echo 'export PATH="$PATH:/path/to/feedbackflow"' >> ~/.zshrc  # if using zsh

# OR create a symlink
sudo ln -s /path/to/feedbackflow/ff /usr/local/bin/ff
```

Once installed globally, you can use the command from anywhere:

```bash
# Run from any directory
ff ./your-project
```

This will:

1. Add FeedbackFlow information to your `~/.cursorrules` file, which helps Cursor AI understand how to use the FeedbackFlow API in your projects.
2. Create a `.github/copilot-instructions.md` file in your project directory, which provides GitHub Copilot with detailed instructions on how to use FeedbackFlow.

### What's Included

#### .cursorrules

The `ff` command adds FeedbackFlow information to your `~/.cursorrules` file, including:

- Description of FeedbackFlow capabilities
- Code examples for sending feedback
- Integration patterns for websites

If you already have a `.cursorrules` file (either in your home directory or in the target project), the `ff` command will intelligently merge the FeedbackFlow information with your existing configuration instead of overwriting it.

#### .github/copilot-instructions.md

The `ff` command creates a `.github/copilot-instructions.md` file in your project directory, including:

- Basic usage examples
- Response handling
- Integration examples (feedback buttons, forms)
- Best practices

If you already have a `.github/copilot-instructions.md` file, the `ff` command will intelligently merge the FeedbackFlow information with your existing instructions instead of overwriting them.

These files make it easier for AI assistants to help you integrate FeedbackFlow into your websites.

## Model Context Protocol (MCP) Integration

FeedbackFlow now supports the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), which allows AI assistants to directly access and interact with your feedback log, creating a seamless AI-driven development cycle.

### Setup

The MCP server can be set up during the FeedbackFlow installation process or separately:

1. **During Installation**:
   - When running `setup.py`, you'll be asked if you want to set up the MCP server
   - If you choose yes, the script will install the necessary dependencies and set up the server

2. **Separate Setup**:
   - Run `python install_mcp.py` to install the MCP dependencies and set up the server
   - Or use the command-line tool: `./ff-mcp install`

### Running the MCP Server

There are several ways to run the MCP server:

1. **Using the Command-Line Tool**:
   - Start the server: `./ff-mcp start`
   - Start with specific options: `./ff-mcp start --transport sse --port 8080`
   - Stop the service: `./ff-mcp stop`
   - Check status: `./ff-mcp status`

2. **Direct Execution**:
   - Run `python mcp_server.py` to start the server directly
   - Press Ctrl+C to stop the server

3. **Helper Script**:
   - Run `python run_mcp_server.py` which handles dependency checking and graceful shutdown

4. **As a Service** (Linux/macOS with systemd):
   - After setup, the server can run as a systemd service

### Cursor IDE Integration

FeedbackFlow MCP integrates seamlessly with [Cursor IDE](https://cursor.sh/), enabling an AI-driven development cycle:

1. **Quick Setup**:
   ```bash
   ./ff-mcp cursor
   ```
   This command guides you through the setup process and provides instructions for adding FeedbackFlow to Cursor.

2. **AI-Driven Development Cycle**:
   - **Code Generation**: AI in Cursor writes website code with embedded feedback collection using `window.FeedbackFlow.sendFeedback()`
   - **Feedback Collection**: During testing, the website automatically sends feedback about user interactions and errors
   - **Feedback Analysis**: AI accesses and analyzes this feedback through MCP resources
   - **Code Improvement**: AI makes code adjustments based on the feedback
   - **Feedback Resolution**: AI marks feedback as addressed, completing the loop

3. **Example Workflow**:
   ```javascript
   // AI-generated code for error tracking
   try {
     // Complex operation
   } catch (error) {
     window.FeedbackFlow.sendFeedback(
       `Error occurred: ${error.message}`,
       'payment-form.js',
       {severity: 'high', component: 'PaymentProcessor'}
     );
   }
   ```

   Later, in Cursor:
   ```
   // AI accesses feedback
   feedback_data = await read_resource("feedback://log")
   
   // AI marks issue as resolved after fixing
   await invoke_tool("mark_feedback_addressed", {
     "timestamp": "2023-01-01 12:34:56",
     "resolution": "Improved error handling in payment form"
   })
   ```

This creates a powerful self-improving system where the AI can continuously refine both the application code and the feedback collection mechanisms.

For more detailed information about the MCP integration and Cursor setup, see [MCP_README.md](MCP_README.md).

## Using with npx

FeedbackFlow can be used directly with `npx` without installing it globally:

```bash
# Show help
npx feedbackflow --help

# Read feedback
npx feedbackflow read

# Clear feedback
npx feedbackflow clear

# Add feedback to Cursor composer
npx feedbackflow add-to-composer

# MCP commands
npx feedbackflow mcp start
npx feedbackflow mcp stop
npx feedbackflow mcp cursor
```

## Using with uv (Recommended for Python Users)

Since FeedbackFlow is primarily a Python project, you can also install and use it with `uv`, the fast Python package installer:

```bash
# Install with uv
python install_with_uv.py
```

Or using npm:
```bash
npm run install-with-uv
```

After installation with `uv`, you can use FeedbackFlow from anywhere:

```bash
# Show help
feedbackflow --help

# Read feedback
feedbackflow read

# MCP commands
feedbackflow mcp start --cursor
```

## Global Installation

You can install FeedbackFlow globally to use it without `npx`:

```bash
# Install globally
npm run install-global

# Or manually
npm install -g .
```

After global installation, you can use FeedbackFlow from anywhere:

```bash
feedbackflow --help
feedbackflow read
feedbackflow mcp start --cursor
```

### Adding to Cursor's MCP Settings

You can add FeedbackFlow to Cursor's MCP settings in two ways:

#### Method 1: Using the Cursor UI

1. Go to `Cursor Settings` > `MCP`
2. Click "Add New MCP Server"
3. Fill out the form with the following information:

**For the stdio transport (recommended):**
- **Name**: FeedbackFlow
- **Type**: command
- **Command**: `npx ff-mcp start --cursor` or if you've installed FeedbackFlow globally: `feedbackflow mcp start --cursor`

**IMPORTANT**: If using a direct path to the script instead of npx, you MUST use an absolute path:
- **Command**: `/absolute/path/to/ff-mcp` (not `./ff-mcp`)
- **Args**: `start --cursor`

You can find the absolute path using:
```bash
which ff-mcp  # On macOS/Linux
where ff-mcp  # On Windows
```

**OR if you prefer using the SSE transport:**
- **Name**: FeedbackFlow
- **Type**: sse
- **URL**: `http://localhost:8080`

For more detailed instructions and troubleshooting, see the [Cursor Integration section in MCP_README.md](MCP_README.md#setting-up-feedbackflow-in-cursor).

#### Method 2: Editing Settings JSON

Add the following to your Cursor settings JSON:

```json
"mcp.commands": {
  "feedbackflow": {
    "name": "FeedbackFlow",
    "command": "npx",
    "args": ["ff-mcp", "start", "--cursor"]
  }
}
```

### Troubleshooting MCP Integration

If you encounter a "Failed to create client" error when adding FeedbackFlow to Cursor's MCP settings, try these solutions:

1. **Use absolute paths**: When configuring the MCP server, use absolute paths instead of relative paths:
   ```json
   "mcp.commands": {
     "feedbackflow": {
       "name": "FeedbackFlow",
       "command": "/absolute/path/to/feedbackflow",
       "args": ["mcp", "start", "--cursor"]
     }
   }
   ```

2. **Restart Cursor**: After making configuration changes, restart Cursor completely.

3. **Verify the server is running**: Make sure the FeedbackFlow MCP server is running before connecting:
   ```bash
   # Check if the server is running
   feedbackflow mcp start --cursor
   ```

4. **Check Cursor logs**: Look for MCP-related errors in Cursor's logs:
   - On macOS: Open Console app and search for "Cursor"
   - On Windows: Check the Event Viewer
   - On Linux: Check `~/.config/Cursor/logs/`

5. **Verify permissions**: Ensure the FeedbackFlow executable has proper permissions.

6. **Try the SSE transport**: If stdio transport isn't working, try the SSE transport instead:
   ```json
   "mcp.commands": {
     "feedbackflow": {
       "name": "FeedbackFlow",
       "command": "feedbackflow",
       "args": ["mcp", "start", "--transport", "sse", "--port", "8080"]
     }
   }
   ```
   Then connect using the URL `http://localhost:8080` in Cursor's MCP settings.

7. **Run the server manually**: Start the MCP server in a separate terminal and connect to it using the SSE transport in Cursor.

For more detailed troubleshooting, see the [MCP_README.md](MCP_README.md) file.

