#!/usr/bin/env python3

import os
import sys
import platform
import subprocess
import shutil

def install_ff_globally():
    """Install the ff command globally on the system."""
    print("=== Installing FeedbackFlow 'ff' Command Globally ===\n")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ff_path = os.path.join(current_dir, "ff")
    ff_py_path = os.path.join(current_dir, "ff.py")
    
    # Check if ff and ff.py exist
    if not os.path.exists(ff_py_path):
        print(f"Error: {ff_py_path} not found")
        sys.exit(1)
    
    if platform.system() == "Windows":
        ff_bat_path = os.path.join(current_dir, "ff.bat")
        if not os.path.exists(ff_bat_path):
            print(f"Error: {ff_bat_path} not found")
            sys.exit(1)
            
        # Add to PATH on Windows
        try:
            print("Adding FeedbackFlow directory to PATH...")
            subprocess.run(f'setx PATH "%PATH%;{current_dir}"', shell=True, check=True)
            print("✅ Added FeedbackFlow directory to PATH")
            print("You'll need to restart your command prompt for the changes to take effect.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error adding to PATH: {e}")
            print("You can manually add the directory to your PATH:")
            print(f'  setx PATH "%PATH%;{current_dir}"')
    else:
        # Unix-like systems (macOS, Linux)
        if not os.path.exists(ff_path):
            print(f"Error: {ff_path} not found")
            sys.exit(1)
            
        # Make ff executable
        try:
            os.chmod(ff_path, 0o755)  # rwxr-xr-x
            print(f"✅ Made {ff_path} executable")
        except Exception as e:
            print(f"❌ Error making ff executable: {e}")
            
        # Create symlink
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
            print(f'  echo \'export PATH="$PATH:{current_dir}"\' >> ~/.bashrc')
            print(f'  echo \'export PATH="$PATH:{current_dir}"\' >> ~/.zshrc  # if using zsh')
    
    print("\n🎉 Installation complete!")
    print("\nYou can now use the 'ff' command from anywhere to add FeedbackFlow AI assistant integration to any project:")
    print("  ff ./your-project-directory")

if __name__ == "__main__":
    install_ff_globally() 