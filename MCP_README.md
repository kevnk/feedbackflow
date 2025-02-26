# FeedbackFlow MCP Integration

This document explains how to use the Model Context Protocol (MCP) integration with FeedbackFlow.

## What is MCP?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open protocol that enables seamless integration between LLM applications (like Claude, ChatGPT, etc.) and external data sources and tools. By integrating FeedbackFlow with MCP, you can allow your AI assistants to directly access and interact with your feedback log.

## Features

The FeedbackFlow MCP server provides the following capabilities:

1. **Resources**:
   - `feedback://log` - Get the contents of the feedback log file
   - `feedback://status` - Get status information about the feedback log file

2. **Tools**:
   - `add_feedback(message)` - Add a new feedback entry to the log file
   - `clear_feedback()` - Clear the feedback log file

3. **Prompts**:
   - `analyze_feedback()` - A prompt template for analyzing feedback data

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
   - Stop the service: `./ff-mcp stop`
   - Check status: `./ff-mcp status`

2. **Direct Execution**:
   - Run `python mcp_server.py` to start the server directly
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

## Using with AI Assistants

Once the MCP server is running, AI assistants that support MCP can connect to it. The server runs on the default MCP port (8080) and provides access to your feedback log.

### Example Usage

Here's how an AI assistant might interact with your feedback log:

1. **Reading Feedback**:
   ```python
   # The AI assistant would use something like:
   feedback_data = await read_resource("feedback://log")
   ```

2. **Adding Feedback**:
   ```python
   # The AI assistant would use something like:
   result = await invoke_tool("add_feedback", {"message": "This feature is great!"})
   ```

3. **Analyzing Feedback**:
   ```python
   # The AI assistant would use the analyze_feedback prompt
   analysis_prompt = await get_prompt("analyze_feedback")
   ```

## Troubleshooting

If you encounter issues with the MCP server:

1. **Check Dependencies**:
   - Ensure the MCP SDK is installed: `pip install mcp[cli]`

2. **Check Server Status**:
   - If running as a service: `systemctl --user status feedbackflow-mcp.service`
   - If running directly, check the terminal output for errors

3. **Port Conflicts**:
   - The MCP server uses port 8080 by default
   - If another application is using this port, you may need to modify the server configuration

## Additional Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Specification](https://github.com/modelcontextprotocol/specification) 