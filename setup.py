#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import json
import shutil

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
    print("Creating extension icons in chrome-extension/images directory...")
    try:
        subprocess.check_call([sys.executable, "scripts/create_icons.py"])
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

def setup_mcp():
    """Set up the Model Context Protocol server."""
    print("\nWould you like to set up the Model Context Protocol (MCP) server? (Y/n)")
    print("This allows AI assistants to access and interact with your feedback log.")
    choice = input().strip().lower()
    
    if choice == 'y' or choice == 'yes' or choice == '':
        print("\nSetting up MCP server...")
        try:
            subprocess.check_call([sys.executable, "mcp/install_mcp.py"])
            print("✅ MCP server setup complete.")
        except subprocess.CalledProcessError:
            print("❌ Error setting up MCP server.")
            print("You can run the setup manually later with: python mcp/install_mcp.py")
    else:
        print("\nSkipping MCP server setup.")
        print("You can set it up later by running: python mcp/install_mcp.py")

def make_ff_executable():
    """Make the ff command executable and offer to install it globally."""
    print("\nMaking the 'ff' command executable...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Make the ff script executable on Unix-like systems
    if platform.system() != "Windows":
        ff_path = os.path.join(current_dir, "cli/ff")
        try:
            os.chmod(ff_path, 0o755)  # rwxr-xr-x
            print(f"✅ Made {ff_path} executable")
        except Exception as e:
            print(f"❌ Error making ff executable: {e}")
    
    # Ask if user wants to install ff globally
    print("\nWould you like to make the 'ff' command available globally? (Y/n)")
    choice = input().strip().lower()
    
    if choice == 'y' or choice == 'yes' or choice == '':
        if platform.system() == "Windows":
            # Add to PATH on Windows
            try:
                subprocess.run(f'setx PATH "%PATH%;{current_dir}"', shell=True, check=True)
                print("✅ Added FeedbackFlow directory to PATH")
                print("You'll need to restart your command prompt for the changes to take effect.")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error adding to PATH: {e}")
                print("You can manually add the directory to your PATH:")
                print(f'  setx PATH "%PATH%;{current_dir}"')
        else:
            # Create symlink on Unix-like systems
            try:
                # Check if /usr/local/bin exists and is writable
                if os.path.exists("/usr/local/bin") and os.access("/usr/local/bin", os.W_OK):
                    symlink_path = "/usr/local/bin/ff"
                    # Remove existing symlink if it exists
                    if os.path.exists(symlink_path):
                        os.remove(symlink_path)
                    os.symlink(ff_path, symlink_path)
                    print(f"✅ Created symlink at {symlink_path}")
                else:
                    # Try with sudo
                    print("Creating symlink requires administrator privileges...")
                    subprocess.run(f"sudo ln -sf {ff_path} /usr/local/bin/ff", shell=True, check=True)
                    print("✅ Created symlink at /usr/local/bin/ff")
            except (OSError, subprocess.CalledProcessError) as e:
                print(f"❌ Error creating symlink: {e}")
                print("\nAlternatively, you can add this directory to your PATH:")
                print(f'  echo \'export PATH="$PATH:{current_dir}/cli"\' >> ~/.bashrc')
                print(f'  echo \'export PATH="$PATH:{current_dir}/cli"\' >> ~/.zshrc  # if using zsh')
    else:
        # Print usage instructions
        print("\nYou can use the 'ff' command to add FeedbackFlow AI assistant integration to any project:")
        print(f"  {current_dir}/cli/ff ./your-project-directory")
        print("\nFor easier access later, you can add this directory to your PATH or create a symlink:")
        
        if platform.system() == "Windows":
            print("\nOn Windows:")
            print(f'  setx PATH "%PATH%;{current_dir}/cli"')
        else:
            print("\nOn macOS/Linux:")
            print(f'  echo \'export PATH="$PATH:{current_dir}/cli"\' >> ~/.bashrc')
            print(f'  echo \'export PATH="$PATH:{current_dir}/cli"\' >> ~/.zshrc  # if using zsh')
            print("  Or create a symlink:")
            print(f"  sudo ln -s {current_dir}/cli/ff /usr/local/bin/ff")

def setup_extension():
    """Set up the Chrome extension."""
    print("\nExtension setup complete!")
    print("\nTo load the extension in Chrome:")
    print("1. Open Chrome and navigate to chrome://extensions/")
    print("2. Enable 'Developer mode' in the top-right corner")
    print("3. Click 'Load unpacked' and select the 'chrome-extension' directory")
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
    
    # Set up MCP server
    setup_mcp()
    
    # Make ff executable
    make_ff_executable()
    
    # Set up extension
    setup_extension()
    
    print("\nSetup complete! You can now use the Feedback Flow extension.")
    print("\nTo add FeedbackFlow AI assistant integration to a project, use the 'ff' command:")
    print("  ./cli/ff ./your-project-directory")
    print("\nIf you set up the MCP server, AI assistants can now access and interact with your feedback log.")

if __name__ == "__main__":
    main() 