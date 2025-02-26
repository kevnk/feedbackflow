#!/usr/bin/env python3
import os
import time
import json
import argparse
import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP, Context

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="FeedbackFlow MCP Server")
    parser.add_argument("--port", type=int, default=8080, help="Port to run the server on")
    parser.add_argument("--transport", type=str, default="sse", choices=["sse", "stdio"], 
                        help="Transport protocol to use (sse or stdio)")
    parser.add_argument("--cursor", action="store_true", help="Configure for Cursor IDE integration")
    return parser.parse_args()

# Parse command line arguments
args = parse_args()

# Create an MCP server for FeedbackFlow
mcp = FastMCP("FeedbackFlow", 
              description="Provides access to website feedback collected by the FeedbackFlow Chrome extension",
              dependencies=["mcp"])

# Get the home directory
home_dir = str(Path.home())
feedback_dir = os.path.join(home_dir, '.feedbackflow')
feedback_log_path = os.path.join(feedback_dir, 'feedback.log')
feedback_meta_path = os.path.join(feedback_dir, 'feedback_meta.json')

@mcp.resource("feedback://log")
def get_feedback_log() -> str:
    """
    Get the contents of the feedback log file.
    
    Returns:
        The contents of the feedback log file as a string.
    """
    try:
        if os.path.exists(feedback_log_path):
            with open(feedback_log_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return "Feedback log file does not exist."
    except Exception as e:
        return f"Error reading feedback log: {str(e)}"

@mcp.resource("feedback://status")
def get_feedback_status() -> dict:
    """
    Get the status of the feedback log file.
    
    Returns:
        A dictionary containing information about the feedback log file.
    """
    try:
        if os.path.exists(feedback_log_path):
            stats = os.stat(feedback_log_path)
            return {
                "exists": True,
                "size_bytes": stats.st_size,
                "last_modified": time.ctime(stats.st_mtime),
                "path": feedback_log_path
            }
        else:
            return {
                "exists": False,
                "path": feedback_log_path
            }
    except Exception as e:
        return {
            "error": str(e)
        }

@mcp.resource("feedback://meta")
def get_feedback_meta() -> dict:
    """
    Get metadata about feedback entries, including source websites and context.
    
    Returns:
        A dictionary containing metadata about feedback entries.
    """
    try:
        if os.path.exists(feedback_meta_path):
            with open(feedback_meta_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {"entries": []}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def add_feedback(message: str, source: str = None, context: dict = None) -> str:
    """
    Add a new feedback entry to the log file.
    
    Args:
        message: The feedback message to add.
        source: The source of the feedback (e.g., website URL).
        context: Additional context about the feedback (e.g., user info, related code).
        
    Returns:
        A confirmation message.
    """
    try:
        # Ensure the directory exists
        os.makedirs(feedback_dir, exist_ok=True)
        
        # Format the feedback entry with timestamp
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        entry = f"[{timestamp}] {message}\n\n"
        
        # Write to the log file
        with open(feedback_log_path, 'a', encoding='utf-8') as f:
            f.write(entry)
        
        # Update metadata
        meta = {"entries": []}
        if os.path.exists(feedback_meta_path):
            try:
                with open(feedback_meta_path, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
            except:
                pass
        
        # Add new entry metadata
        meta["entries"].append({
            "timestamp": timestamp,
            "message": message,
            "source": source,
            "context": context
        })
        
        # Write updated metadata
        with open(feedback_meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2)
        
        return f"Feedback added successfully at {timestamp}"
    except Exception as e:
        return f"Error adding feedback: {str(e)}"

@mcp.tool()
def clear_feedback() -> str:
    """
    Clear the feedback log file.
    
    Returns:
        A confirmation message.
    """
    try:
        # Ensure the directory exists
        os.makedirs(feedback_dir, exist_ok=True)
        
        # Clear the log file by opening it in write mode
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(feedback_log_path, 'w', encoding='utf-8') as f:
            f.write(f"# Feedback Flow Log File - Cleared on {timestamp}\n")
        
        # Clear metadata
        with open(feedback_meta_path, 'w', encoding='utf-8') as f:
            json.dump({"entries": []}, f, indent=2)
        
        return f"Feedback log cleared successfully at {timestamp}"
    except Exception as e:
        return f"Error clearing feedback log: {str(e)}"

@mcp.tool()
def mark_feedback_addressed(timestamp: str, resolution: str = None) -> str:
    """
    Mark a feedback entry as addressed.
    
    Args:
        timestamp: The timestamp of the feedback entry to mark as addressed.
        resolution: Optional description of how the feedback was addressed.
        
    Returns:
        A confirmation message.
    """
    try:
        if not os.path.exists(feedback_meta_path):
            return "Feedback metadata file does not exist."
        
        # Load metadata
        with open(feedback_meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        
        # Find and update the entry
        found = False
        for entry in meta.get("entries", []):
            if entry.get("timestamp") == timestamp:
                entry["addressed"] = True
                entry["resolution"] = resolution
                entry["addressed_at"] = time.strftime('%Y-%m-%d %H:%M:%S')
                found = True
                break
        
        if not found:
            return f"No feedback entry found with timestamp {timestamp}"
        
        # Write updated metadata
        with open(feedback_meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2)
        
        return f"Feedback entry marked as addressed"
    except Exception as e:
        return f"Error marking feedback as addressed: {str(e)}"

@mcp.prompt()
def analyze_feedback() -> str:
    """
    Prompt for analyzing the feedback in the log file.
    """
    return """
    Please analyze the feedback in the log file and provide insights on:
    1. Common themes or patterns
    2. Sentiment analysis (positive, negative, neutral)
    3. Actionable suggestions based on the feedback
    4. Any urgent issues that need immediate attention
    
    Format your response in a clear, structured way with sections for each of the above points.
    """

@mcp.prompt()
def cursor_integration_guide() -> str:
    """
    Prompt for guiding users on how to integrate FeedbackFlow with Cursor.
    """
    return """
    # FeedbackFlow Integration with Cursor
    
    To effectively use FeedbackFlow with Cursor, follow these steps:
    
    ## Setup
    
    1. Ensure the FeedbackFlow MCP server is running:
       ```bash
       ./ff-mcp start
       ```
    
    2. In Cursor, go to Settings > Features > MCP Servers
    
    3. Add a new MCP server with:
       - Name: FeedbackFlow
       - Command: ./ff-mcp start --cursor
       - Or URL: http://localhost:8080 (if using SSE transport)
    
    ## Using FeedbackFlow in Cursor
    
    When working with code that uses FeedbackFlow, you can:
    
    1. Access the feedback log:
       - Use the resource `feedback://log` to view all feedback
       - Use the resource `feedback://status` to check the log status
       - Use the resource `feedback://meta` to get detailed metadata
    
    2. Manage feedback:
       - Use the tool `add_feedback` to add new feedback entries
       - Use the tool `clear_feedback` to clear the log
       - Use the tool `mark_feedback_addressed` to mark entries as resolved
    
    3. Analyze feedback:
       - Use the prompt `analyze_feedback` to get insights from the feedback
    
    ## Example Workflow
    
    1. Review recent feedback: `feedback://log`
    2. Identify issues to address in the code
    3. Make code changes to address the feedback
    4. Mark the feedback as addressed: `mark_feedback_addressed`
    5. Test the changes to ensure they resolve the feedback
    
    This workflow helps maintain a continuous feedback loop between your website users and your development process.
    """

def print_cursor_instructions():
    """Print instructions for adding the MCP server to Cursor."""
    print("\n=== Cursor Integration Instructions ===")
    print("\nTo add FeedbackFlow MCP to Cursor:")
    print("1. Open Cursor IDE")
    print("2. Go to Settings > Features > MCP Servers")
    print("3. Click 'Add New MCP Server'")
    print("4. Use the following settings:")
    if args.transport == "stdio":
        print("   - Name: FeedbackFlow")
        print(f"   - Command: {sys.executable} {os.path.abspath(__file__)} --cursor")
    else:  # sse
        print("   - Name: FeedbackFlow")
        print(f"   - URL: http://localhost:{args.port}")
    print("\nThe MCP server is now running and ready for Cursor to connect.")
    print("You can use FeedbackFlow resources and tools in Cursor's Composer and Agent features.")

if __name__ == "__main__":
    # Ensure the feedback directory exists
    os.makedirs(feedback_dir, exist_ok=True)
    
    # Run the MCP server
    if args.cursor:
        print("Starting FeedbackFlow MCP server in Cursor mode...")
        # When run from Cursor, use stdio transport
        mcp.run(transport="stdio")
    else:
        print(f"Starting FeedbackFlow MCP server on port {args.port} with {args.transport} transport...")
        if args.transport == "stdio":
            mcp.run(transport="stdio")
        else:
            mcp.run(port=args.port)
            
        # Print Cursor integration instructions if not already in Cursor mode
        print_cursor_instructions() 