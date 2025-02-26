#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
from pathlib import Path

def install_mcp_dependencies():
    """Install MCP Python SDK and dependencies."""
    print("Installing MCP Python SDK and dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mcp[cli]"])
        print("✅ MCP Python SDK installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing MCP Python SDK: {e}")
        print("You can manually install it with: pip install mcp[cli]")
        return False
    return True

def create_mcp_service():
    """Create a service file for the MCP server on Linux/macOS."""
    if platform.system() == "Windows":
        print("Service creation is not supported on Windows.")
        print("You can manually run the MCP server with: python mcp_server.py")
        return
    
    # Get the home directory
    home_dir = str(Path.home())
    
    # Create the service directory if it doesn't exist
    service_dir = os.path.join(home_dir, '.config', 'systemd', 'user')
    os.makedirs(service_dir, exist_ok=True)
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create the service file
    service_path = os.path.join(service_dir, 'feedbackflow-mcp.service')
    service_content = f"""[Unit]
Description=FeedbackFlow MCP Server
After=network.target

[Service]
ExecStart={sys.executable} {os.path.join(current_dir, 'mcp_server.py')}
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=default.target
"""
    
    try:
        with open(service_path, 'w') as f:
            f.write(service_content)
        
        print(f"✅ Created service file at {service_path}")
        print("To enable and start the service, run:")
        print("  systemctl --user daemon-reload")
        print("  systemctl --user enable feedbackflow-mcp.service")
        print("  systemctl --user start feedbackflow-mcp.service")
    except Exception as e:
        print(f"❌ Error creating service file: {e}")
        print("You can manually run the MCP server with: python mcp_server.py")

def main():
    """Main function to install MCP dependencies and set up the server."""
    print("=== FeedbackFlow MCP Server Setup ===\n")
    
    # Install MCP dependencies
    if not install_mcp_dependencies():
        return
    
    # Create service file
    create_mcp_service()
    
    print("\nMCP server setup complete!")
    print("\nYou can now run the MCP server with:")
    print("  python mcp_server.py")
    print("\nThis will allow AI assistants to access and interact with your feedback log.")

if __name__ == "__main__":
    main() 