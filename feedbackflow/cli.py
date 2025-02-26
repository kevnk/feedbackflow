#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
from pathlib import Path

def get_package_dir():
    """Get the directory where the feedbackflow package is installed."""
    return os.path.dirname(os.path.abspath(__file__))

def get_project_dir():
    """Get the directory of the FeedbackFlow project."""
    package_dir = get_package_dir()
    # The project directory is the parent of the package directory
    return os.path.dirname(package_dir)

def run_script(script_name, args=None):
    """Run a Python script from the project directory."""
    if args is None:
        args = []
    
    project_dir = get_project_dir()
    script_path = os.path.join(project_dir, script_name)
    
    if not os.path.exists(script_path):
        print(f"Error: Script {script_name} not found at {script_path}")
        sys.exit(1)
    
    try:
        subprocess.run([sys.executable, script_path] + args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_name}: {e}")
        sys.exit(e.returncode)

def handle_mcp_command(args):
    """Handle MCP-related commands."""
    if len(args) == 0:
        print("Error: Missing MCP subcommand")
        show_mcp_help()
        return
    
    mcp_command = args[0]
    mcp_args = args[1:]
    
    if mcp_command == "start":
        run_script("ff-mcp", ["start"] + mcp_args)
    elif mcp_command == "stop":
        run_script("ff-mcp", ["stop"] + mcp_args)
    elif mcp_command == "install":
        run_script("ff-mcp", ["install"] + mcp_args)
    elif mcp_command == "cursor":
        run_script("ff-mcp", ["cursor"] + mcp_args)
    else:
        print(f"Error: Unknown MCP subcommand: {mcp_command}")
        show_mcp_help()

def show_help():
    """Show help information."""
    print("""
FeedbackFlow CLI - Collect and manage feedback for AI-driven development

Usage:
  feedbackflow <command> [options]

Commands:
  add-to-composer       Add feedback log to Cursor composer
  start-mcp             Start the MCP server
  setup-cursor-mcp      Setup Cursor MCP integration
  install-mcp           Install MCP components
  read                  Read feedback log
  clear                 Clear feedback log
  check-extension       Check if the Chrome extension is installed
  mcp <subcommand>      MCP-related commands (start, stop, install, cursor)

Options:
  --help, -h            Show this help message

For more information, visit: https://github.com/yourusername/feedbackflow
""")

def show_mcp_help():
    """Show MCP-specific help."""
    print("""
FeedbackFlow MCP Commands:

Usage:
  feedbackflow mcp <subcommand> [options]

Subcommands:
  start                 Start the MCP server
  stop                  Stop the MCP server
  install               Install MCP as a service
  cursor                Setup Cursor MCP integration

Options:
  --transport <type>    Transport type (default: sse)
  --port <number>       Port number (default: 8080)
  --cursor              Run in Cursor mode
""")

def main():
    """Main entry point for the CLI."""
    args = sys.argv[1:]
    
    if len(args) == 0 or args[0] in ["--help", "-h"]:
        show_help()
        return
    
    command = args[0]
    command_args = args[1:]
    
    if command == "add-to-composer":
        run_script("add_feedback_to_composer.py", command_args)
    elif command == "start-mcp":
        run_script("mcp_server.py", command_args)
    elif command == "setup-cursor-mcp":
        run_script("ff-mcp", ["cursor"] + command_args)
    elif command == "install-mcp":
        run_script("install_mcp.py", command_args)
    elif command == "read":
        run_script("read_feedback.py", command_args)
    elif command == "clear":
        run_script("clear_feedback.py", command_args)
    elif command == "check-extension":
        run_script("check_extension.py", command_args)
    elif command == "mcp":
        handle_mcp_command(command_args)
    else:
        # Pass all arguments to ff.py for any other commands
        run_script("ff.py", args)

if __name__ == "__main__":
    main() 