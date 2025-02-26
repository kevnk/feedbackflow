# FeedbackLoop Chrome Extension

A Chrome extension that allows you to send feedback from your website to your AI assistant. The feedback is stored in a log file that can be easily accessed by Cursor or VS Code.

## Features

- Send feedback directly from any website using the extension popup
- JavaScript API for websites to send feedback programmatically
- Native messaging host to write feedback to a local log file
- Python script to read and watch the feedback log
- VS Code/Cursor integration via tasks

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
5. The FeedbackLoop extension should now appear in your extensions list

#### 2. Install the Native Messaging Host

The native messaging host allows the extension to write to a log file on your system.

##### Automatic Installation

Run the installation script:

```bash
python native-host/install_host.py
```

This will:
- Install the native messaging host for Chrome
- Create the `.feedbackloop` directory in your home folder
- Create an empty `feedback.log` file

##### Manual Installation

If the automatic installation doesn't work:

1. Update the `native-host/com.feedbackloop.host.json` file:
   - Replace `REPLACE_WITH_ABSOLUTE_PATH` with the absolute path to the `feedbackloop_host.py` script
   - After loading the extension, replace `REPLACE_WITH_EXTENSION_ID` with your extension ID

2. Copy the manifest file to the appropriate location:
   - **macOS**: `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/`
   - **Linux**: `~/.config/google-chrome/NativeMessagingHosts/`
   - **Windows**: Add a registry key (see installation script for details)

3. Make the host script executable:
   ```bash
   chmod +x native-host/feedbackloop_host.py
   ```

## Usage

### Using the Extension Popup

1. Click on the FeedbackLoop extension icon in your browser
2. Type your feedback in the text area
3. Click "Send Feedback"

### Using the JavaScript API in Your Website

The extension injects a JavaScript API into every web page. You can use it like this:

```javascript
// Check if the FeedbackLoop API is available
if (window.FeedbackLoop) {
  // Send feedback
  window.FeedbackLoop.sendFeedback("Your feedback message here");
}

// Listen for responses
window.addEventListener('message', function(event) {
  if (event.source !== window) return;
  
  if (event.data.type && event.data.type === 'FEEDBACK_LOOP_RESPONSE') {
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

Then open http://localhost:8000 in your browser to see a demonstration of how to use the FeedbackLoop API.

## Troubleshooting

If the extension isn't working:

1. Run the check script to verify your setup:
   ```bash
   python check_extension.py
   ```
   
2. Check if the native messaging host is installed correctly
3. Look for errors in the Chrome extension's background page (inspect the extension)
4. Check the error log in the `.feedbackloop` directory in your home folder

