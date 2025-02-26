# FeedbackFlow MCP Integration

This document explains how to use the Model Context Protocol (MCP) integration with FeedbackFlow to create an AI-driven development cycle.

## What is MCP?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open protocol that enables seamless integration between LLM applications (like Claude, ChatGPT, etc.) and external data sources and tools. By integrating FeedbackFlow with MCP, you can create a self-improving AI development system where AI assistants both generate feedback collection code and respond to the feedback received.

## Features

The FeedbackFlow MCP server provides the following capabilities:

1. **Resources**:
   - `feedback://log` - Get the contents of the feedback log file
   - `feedback://status` - Get status information about the feedback log file
   - `feedback://meta` - Get metadata about feedback entries, including source and context

2. **Tools**:
   - `add_feedback(message, source, context)` - Add a new feedback entry to the log file
   - `clear_feedback()` - Clear the feedback log file
   - `mark_feedback_addressed(timestamp, resolution)` - Mark a feedback entry as addressed

3. **Prompts**:
   - `analyze_feedback()` - A prompt template for analyzing feedback data
   - `cursor_integration_guide()` - A guide for integrating FeedbackFlow with Cursor

## Setup

The MCP server can be set up during the FeedbackFlow installation process or separately:

1. **During Installation**:
   - When running `setup.py`, you'll be asked if you want to set up the MCP server
   - If you choose yes, the script will install the necessary dependencies and set up the server

2. **Separate Setup**:
   - Run `python install_mcp.py` to install the MCP dependencies and set up the server
   - Or use the command-line tool: `./ff-mcp install`

## Running the MCP Server

There are several ways to run the MCP server:

1. **Using the Command-Line Tool**:
   - Start the server: `./ff-mcp start`
   - Start with specific options: `./ff-mcp start --transport sse --port 8080`
   - Start for Cursor integration: `./ff-mcp start --cursor`
   - Stop the service: `./ff-mcp stop`
   - Check status: `./ff-mcp status`

2. **Direct Execution**:
   - Run `python mcp_server.py` to start the server directly
   - Use options: `python mcp_server.py --transport sse --port 8080`
   - Press Ctrl+C to stop the server

3. **Helper Script**:
   - Run `python run_mcp_server.py` which handles dependency checking and graceful shutdown

4. **As a Service** (Linux/macOS with systemd):
   - After setup, enable and start the service:
     ```
     systemctl --user daemon-reload
     systemctl --user enable feedbackflow-mcp.service
     systemctl --user start feedbackflow-mcp.service
     ```
   - Check status with: `systemctl --user status feedbackflow-mcp.service`
   - Stop with: `systemctl --user stop feedbackflow-mcp.service`

## Cursor Integration

FeedbackFlow MCP can be integrated with [Cursor IDE](https://cursor.sh/) to enable a seamless AI-driven development cycle.

### Setting Up FeedbackFlow in Cursor

1. **Quick Setup**:
   - Run the dedicated setup command: `./ff-mcp cursor`
   - This will guide you through the setup process and provide instructions

2. **Manual Setup**:
   - Open Cursor IDE
   - Go to Settings > Features > MCP Servers
   - Click "Add New MCP Server"
   - Configure with:
     - Name: FeedbackFlow
     - Type: command
     - Command: `npx ff-mcp start --cursor` or if you've installed FeedbackFlow globally: `feedbackflow mcp start --cursor`

   **⚠️ IMPORTANT**: If using a direct path to the script instead of npx, you MUST use an absolute path:
     - Command: `/absolute/path/to/ff-mcp` (not `./ff-mcp`)
     - Args: `start --cursor`

   You can find the absolute path using:
   ```bash
   which ff-mcp  # On macOS/Linux
   where ff-mcp  # On Windows
   ```

   **OR if you prefer using the SSE transport:**
     - Name: FeedbackFlow
     - Type: sse
     - URL: `http://localhost:8080`

3. **Verifying the Connection**:
   - In Cursor's Composer, try accessing a FeedbackFlow resource
   - For example, ask "Show me the feedback log" or "Get the feedback status"
   - If working correctly, you should see the feedback data in the response

### AI-Driven Development Cycle

The primary purpose of the FeedbackFlow MCP integration is to enable an AI-driven development cycle:

1. **Code Generation**:
   - AI in Cursor writes website code with embedded feedback collection
   - Uses the `window.FeedbackFlow.sendFeedback()` API to collect feedback programmatically
   - Can instrument code to automatically report errors, user interactions, and performance metrics

2. **Feedback Collection**:
   - During testing and development, the website automatically sends feedback
   - Feedback is collected with context about where and why it was generated
   - This happens without requiring manual user intervention

3. **Feedback Analysis**:
   - AI accesses and analyzes this feedback through MCP resources
   - Can identify patterns, recurring issues, and areas for improvement
   - Uses the feedback to guide further development

4. **Code Improvement**:
   - AI makes code adjustments based on the feedback
   - Can refine both the application code and the feedback collection mechanisms
   - Creates a continuous improvement loop

5. **Feedback Resolution**:
   - AI marks feedback as addressed using the `mark_feedback_addressed` tool
   - Maintains a documented history of issues and resolutions
   - Completes the development cycle

### Using FeedbackFlow in Cursor

Once connected, you can use FeedbackFlow's resources and tools directly in Cursor's Composer and Agent features:

1. **Generating Feedback Collection Code**:
   ```javascript
   // AI-generated code for a button that sends feedback
   document.getElementById('submit-btn').addEventListener('click', () => {
     window.FeedbackFlow.sendFeedback(
       `User submitted form with data: ${JSON.stringify(formData)}`,
       'contact-form.js',
       {action: 'submit', formId: 'contact'}
     );
   });
   
   // AI-generated code for error tracking
   try {
     // Some complex operation
   } catch (error) {
     window.FeedbackFlow.sendFeedback(
       `Error occurred: ${error.message}`,
       'payment-processor.js',
       {severity: 'high', component: 'PaymentProcessor'}
     );
   }
   
   // AI-generated code for performance monitoring
   const startTime = performance.now();
   // Operation to measure
   const endTime = performance.now();
   if (endTime - startTime > 500) {  // If operation takes more than 500ms
     window.FeedbackFlow.sendFeedback(
       `Performance issue: Operation took ${endTime - startTime}ms`,
       'image-gallery.js',
       {operation: 'loadImages', duration: endTime - startTime}
     );
   }
   ```

2. **Accessing Feedback**:
   ```
   # The AI assistant would use:
   feedback_data = await read_resource("feedback://log")
   
   # Or with metadata:
   feedback_meta = await read_resource("feedback://meta")
   ```

3. **Analyzing Feedback**:
   ```
   # The AI assistant would use:
   analysis_prompt = await get_prompt("analyze_feedback")
   
   # Then apply the prompt to the feedback data
   ```

4. **Adding New Feedback**:
   ```
   # The AI assistant might add feedback directly:
   result = await invoke_tool("add_feedback", {
     "message": "Identified potential memory leak in image carousel",
     "source": "code-review",
     "context": {"file": "carousel.js", "severity": "medium"}
   })
   ```

5. **Marking Feedback as Addressed**:
   ```
   # After fixing an issue, the AI would mark it as addressed:
   result = await invoke_tool("mark_feedback_addressed", {
     "timestamp": "2023-01-01 12:34:56",
     "resolution": "Fixed memory leak by properly removing event listeners"
   })
   ```

### Example Complete Workflow

Here's a complete example of the AI-driven development cycle:

1. **Initial Code Generation**:
   AI in Cursor generates a website feature with feedback collection:
   ```javascript
   // User registration form handler
   document.getElementById('register-form').addEventListener('submit', (event) => {
     event.preventDefault();
     const email = document.getElementById('email').value;
     const password = document.getElementById('password').value;
     
     try {
       // Attempt to register user
       registerUser(email, password);
       
       // Send success feedback
       window.FeedbackFlow.sendFeedback(
         `User registered successfully: ${email}`,
         'register.js',
         {action: 'register', status: 'success'}
       );
     } catch (error) {
       // Send error feedback
       window.FeedbackFlow.sendFeedback(
         `Registration error: ${error.message}`,
         'register.js',
         {action: 'register', status: 'error', message: error.message}
       );
       
       // Show error to user
       showError(error.message);
     }
   });
   ```

2. **Testing and Feedback Collection**:
   During testing, the website automatically sends feedback about registration attempts.

3. **Feedback Analysis**:
   In Cursor, the AI accesses and analyzes the feedback:
   ```
   // Get feedback data
   feedback_data = await read_resource("feedback://log")
   feedback_meta = await read_resource("feedback://meta")
   
   // Analyze patterns
   // AI identifies that many users are getting password validation errors
   ```

4. **Code Improvement**:
   The AI improves the code based on the feedback:
   ```javascript
   // Improved registration form with better validation
   document.getElementById('register-form').addEventListener('submit', (event) => {
     event.preventDefault();
     const email = document.getElementById('email').value;
     const password = document.getElementById('password').value;
     
     // Add client-side validation
     if (password.length < 8) {
       showError('Password must be at least 8 characters long');
       window.FeedbackFlow.sendFeedback(
         `Password validation failed: too short`,
         'register.js',
         {action: 'validate', field: 'password', reason: 'too_short'}
       );
       return;
     }
     
     if (!/[A-Z]/.test(password)) {
       showError('Password must contain at least one uppercase letter');
       window.FeedbackFlow.sendFeedback(
         `Password validation failed: no uppercase`,
         'register.js',
         {action: 'validate', field: 'password', reason: 'no_uppercase'}
       );
       return;
     }
     
     try {
       // Attempt to register user with improved validation
       registerUser(email, password);
       
       // Send success feedback
       window.FeedbackFlow.sendFeedback(
         `User registered successfully: ${email}`,
         'register.js',
         {action: 'register', status: 'success'}
       );
     } catch (error) {
       // Send error feedback with more context
       window.FeedbackFlow.sendFeedback(
         `Registration error: ${error.message}`,
         'register.js',
         {action: 'register', status: 'error', message: error.message}
       );
       
       // Show improved error message to user
       showError(getReadableErrorMessage(error));
     }
   });
   ```

5. **Feedback Resolution**:
   The AI marks the feedback as addressed:
   ```
   // Mark feedback as addressed
   await invoke_tool("mark_feedback_addressed", {
     "timestamp": "2023-01-01 12:34:56",
     "resolution": "Added client-side password validation with clear error messages"
   })
   ```

This cycle can continue indefinitely, with the AI continuously improving the code based on feedback.

## Using with Other AI Assistants

While Cursor integration provides the most seamless experience, any AI assistant that supports MCP can connect to the FeedbackFlow server. The server runs on the default MCP port (8080) and provides access to your feedback log.

## Troubleshooting

If you encounter issues with the MCP server:

1. **Check Dependencies**:
   - Ensure the MCP SDK is installed: `pip install mcp[cli]`

2. **Check Server Status**:
   - If running as a service: `systemctl --user status feedbackflow-mcp.service`
   - If running directly, check the terminal output for errors

3. **Port Conflicts**:
   - The MCP server uses port 8080 by default
   - If another application is using this port, you can specify a different port:
     ```
     ./ff-mcp start --port 8081
     ```

4. **Cursor Integration Issues**:
   - Make sure you're using the correct transport protocol (stdio for direct integration)
   - Verify that the MCP server is running before connecting from Cursor
   - Check Cursor's logs for any connection errors

5. **JavaScript API Issues**:
   - Ensure the Chrome extension is properly installed and active
   - Check the browser console for any errors related to FeedbackFlow
   - Verify that `window.FeedbackFlow` is available in your website's context

## Additional Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Specification](https://github.com/modelcontextprotocol/specification)
- [Cursor MCP Documentation](https://docs.cursor.com/context/model-context-protocol)

## Using FeedbackFlow with npx

FeedbackFlow can be used directly with `npx` without installing it globally. This makes it easy to integrate with Cursor's settings MCP section.

```bash
# Start the MCP server with npx
npx ff-mcp start

# Start for Cursor integration
npx ff-mcp start --cursor
```

## Using FeedbackFlow with uv (Recommended for Python Users)

Since FeedbackFlow is primarily a Python project, you can also install and use it with `uv`, the fast Python package installer.

### Installation

```bash
# Install with uv
python install_with_uv.py

# Or run the npm script
npm run install-with-uv
```

### Basic Usage

```bash
# Show help
feedbackflow --help

# Read feedback
feedbackflow read

# Clear feedback
feedbackflow clear

# Add feedback to Cursor composer
feedbackflow add-to-composer
```

### MCP Commands

```bash
# Start MCP server
feedbackflow mcp start

# Start MCP server with specific options
feedbackflow mcp start --transport sse --port 8080 --cursor

# Stop MCP server
feedbackflow mcp stop

# Setup Cursor MCP integration
feedbackflow mcp cursor
```

### Adding to Cursor's MCP Settings

You can add FeedbackFlow to Cursor's MCP settings in two ways:

#### Method 1: Using the Cursor UI

1. Go to `Cursor Settings` > `Features` > `MCP Servers`
2. Click on the `+ Add New MCP Server` button
3. Fill out the form with the following information:

**For the stdio transport (recommended):**
- **Name**: FeedbackFlow
- **Type**: stdio
- **Command**: `npx ff-mcp start --cursor` or if you've installed FeedbackFlow globally: `feedbackflow mcp start --cursor`

**⚠️ IMPORTANT**: If using a direct path to the script instead of npx, you MUST use an absolute path:
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

After adding the MCP server, it should appear in your list of MCP servers. You might need to press the refresh button in the top right corner of the MCP server section to populate the tool list.

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

**⚠️ IMPORTANT**: If using a direct path to the script instead of npx, you MUST use an absolute path:
```json
"mcp.commands": {
  "feedbackflow": {
    "name": "FeedbackFlow",
    "command": "/absolute/path/to/ff-mcp",
    "args": ["start", "--cursor"]
  }
}
```

Relative paths like `./ff-mcp` will NOT work in Cursor's MCP settings.

#### Project-Specific Configuration

You can also configure FeedbackFlow as a project-specific MCP server by creating a `.cursor/mcp.json` file in your project root:

```json
{
  "mcpServers": {
    "feedbackflow": {
      "command": "feedbackflow",
      "args": ["mcp", "start", "--cursor"]
    }
  }
}
```

This will allow you to start the FeedbackFlow MCP server directly from Cursor's MCP menu.

## Troubleshooting MCP Integration Issues

### "Failed to create client" Error

If you encounter a "Failed to create client" error when adding FeedbackFlow to Cursor's MCP settings, follow this debugging workflow:

1. **Use absolute paths**:
   - **This is critical**: Always use absolute paths in your MCP configuration. Relative paths like `./ff-mcp` will NOT work.
   ```json
   "mcp.commands": {
     "feedbackflow": {
       "name": "FeedbackFlow",
       "command": "/absolute/path/to/ff-mcp",
       "args": ["start", "--cursor"]
     }
   }
   ```
   - You can find the absolute path to the ff-mcp executable by running:
   ```bash
   which ff-mcp  # On macOS/Linux
   where ff-mcp  # On Windows
   ```

2. **Restart after configuration changes**:
   - Always restart the MCP server after making any configuration changes
   - Restart Cursor completely (not just reload window)

3. **Check server availability**:
   - Verify the MCP server is running and accessible before connecting
   - Test the server manually:
   ```bash
   # Start the server in a terminal
   feedbackflow mcp start --cursor
   ```
   - Look for any error messages in the terminal output

4. **Verify transport configuration**:
   - For stdio transport: Ensure the command is executable and properly formatted
   - For SSE transport: Verify the server is running on the specified port
   - Try switching transport methods if one isn't working

5. **Check Cursor logs**:
   - Examine Cursor's logs for detailed error information:
     - On macOS: `~/Library/Application Support/Cursor/logs/`
     - On Windows: `%APPDATA%\Cursor\logs\`
     - On Linux: `~/.config/Cursor/logs/`
   - Look for entries containing "MCP" or "Failed to create client"

6. **Test with a simple MCP server**:
   - Try connecting to a known working MCP server to verify Cursor's MCP functionality
   - The MCP quickstart example can be used for testing: [MCP Quickstart](https://github.com/modelcontextprotocol/quickstart)

7. **Verify network settings**:
   - For SSE transport, ensure no firewall or network settings are blocking the connection
   - Try using localhost (127.0.0.1) instead of a hostname

8. **Check for conflicting processes**:
   - Ensure no other process is using the same port (default 8080)
   - Use a different port if needed:
   ```bash
   feedbackflow mcp start --cursor --port 8081
   ```

9. **Permissions issues**:
   - Ensure the FeedbackFlow executable has proper execution permissions
   - On macOS/Linux: `chmod +x /path/to/feedbackflow`

10. **Manual server and connection**:
    - Start the MCP server manually in a terminal:
    ```bash
    feedbackflow mcp start --transport sse --port 8080
    ```
    - Then in Cursor, add an MCP server with:
      - Type: SSE
      - URL: http://localhost:8080

If you continue to experience issues, please check the Cursor logs for specific error messages and consult the [Cursor MCP Documentation](https://docs.cursor.com/context/model-context-protocol) for additional troubleshooting steps. 