# Feedback Flow Chrome Extension

A Chrome extension that allows you to send feedback from your website to your AI assistant. The feedback is stored in a log file that can be easily accessed by Cursor or VS Code.

## Features

- Send feedback directly from any website using the extension popup
- JavaScript API for websites to send feedback programmatically
- Native messaging host to write feedback to a local log file
- Python script to read and watch the feedback log
- VS Code/Cursor integration via tasks
- Easy addition of feedback log to Cursor composer context

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
- Guide you through loading the extension in Chrome

Alternatively, you can use the VS Code/Cursor task "Setup Extension" to run the setup script.

### Manual Installation

#### 1. Install the Chrome Extension

1. Clone this repository or download it to your local machine
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable "Developer mode" in the top-right corner
4. Click "Load unpacked" and select the root directory of this project
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
python update_extension_id.py YOUR_EXTENSION_ID
```

Replace `YOUR_EXTENSION_ID` with the ID of your extension, which you can find in Chrome's extension management page (chrome://extensions/) after enabling Developer mode.

##### Troubleshooting

If the automatic installation doesn't work:

1. The repository contains an example manifest file (`native-host/com.feedbackflow.host.json.example`). During installation, this file is used as a template to create the actual manifest file with the correct paths.

2. If you need to manually set up the native host:
   - Copy the example manifest file to create `native-host/com.feedbackflow.host.json`
   - Replace `PLACEHOLDER_PATH` with the absolute path to the `feedbackflow_host.py` script
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
   python update_extension_id.py YOUR_EXTENSION_ID
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

