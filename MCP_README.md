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
     - Command: `/path/to/python /path/to/mcp_server.py --cursor`
     - Or URL: `http://localhost:8080` (if using SSE transport)

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