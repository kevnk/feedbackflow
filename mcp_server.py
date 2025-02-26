#!/usr/bin/env python3
import os
import time
from pathlib import Path
from mcp.server.fastmcp import FastMCP, Context

# Create an MCP server for FeedbackFlow
mcp = FastMCP("FeedbackFlow", 
              description="Provides access to website feedback collected by the FeedbackFlow Chrome extension",
              dependencies=["mcp"])

# Get the home directory
home_dir = str(Path.home())
feedback_dir = os.path.join(home_dir, '.feedbackflow')
feedback_log_path = os.path.join(feedback_dir, 'feedback.log')

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

@mcp.tool()
def add_feedback(message: str) -> str:
    """
    Add a new feedback entry to the log file.
    
    Args:
        message: The feedback message to add.
        
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
        
        return f"Feedback log cleared successfully at {timestamp}"
    except Exception as e:
        return f"Error clearing feedback log: {str(e)}"

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

if __name__ == "__main__":
    # Run the MCP server
    mcp.run() 