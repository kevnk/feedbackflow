#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import signal
import platform

def check_mcp_installed():
    """Check if MCP is installed."""
    try:
        import mcp
        return True
    except ImportError:
        return False

def install_mcp():
    """Install MCP if not already installed."""
    print("MCP Python SDK is not installed. Installing now...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mcp[cli]"])
        print("✅ MCP Python SDK installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing MCP Python SDK: {e}")
        print("Please install it manually with: pip install mcp[cli]")
        return False

def run_server():
    """Run the MCP server."""
    # Check if MCP is installed
    if not check_mcp_installed():
        if not install_mcp():
            return
    
    print("Starting FeedbackFlow MCP server...")
    print("Press Ctrl+C to stop the server.")
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\nStopping MCP server...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Run the MCP server
    try:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        server_path = os.path.join(current_dir, "mcp_server.py")
        
        # Run the server
        subprocess.run([sys.executable, server_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running MCP server: {e}")
        sys.exit(1)

def main():
    """Main function."""
    print("=== FeedbackFlow MCP Server ===\n")
    
    # Run the server
    run_server()

if __name__ == "__main__":
    main() 