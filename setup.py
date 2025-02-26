#!/usr/bin/env python3
import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is 3.6 or higher."""
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required.")
        sys.exit(1)

def install_dependencies():
    """Install required Python dependencies."""
    print("Installing required Python packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print("Error: Failed to install dependencies.")
        sys.exit(1)

def create_icons():
    """Create icon files for the extension."""
    print("Creating extension icons...")
    try:
        subprocess.check_call([sys.executable, "create_icons.py"])
    except subprocess.CalledProcessError:
        print("Error: Failed to create icons.")
        sys.exit(1)

def install_native_host():
    """Install the native messaging host."""
    print("Installing native messaging host...")
    try:
        subprocess.check_call([sys.executable, "native-host/install_host.py"])
    except subprocess.CalledProcessError:
        print("Error: Failed to install native messaging host.")
        print("You may need to run the native host installation manually.")
        print("Run: python native-host/install_host.py")

def setup_extension():
    """Set up the Chrome extension."""
    print("\nExtension setup complete!")
    print("\nTo load the extension in Chrome:")
    print("1. Open Chrome and navigate to chrome://extensions/")
    print("2. Enable 'Developer mode' in the top-right corner")
    print("3. Click 'Load unpacked' and select this directory")
    print("4. The Feedback Flow extension should now appear in your extensions list")

def main():
    """Main setup function."""
    print("=== Feedback Flow Extension Setup ===\n")
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create icons
    create_icons()
    
    # Install native host
    install_native_host()
    
    # Set up extension
    setup_extension()
    
    print("\nSetup complete! You can now use the Feedback Flow extension.")

if __name__ == "__main__":
    main() 