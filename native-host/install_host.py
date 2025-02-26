#!/usr/bin/env python3
import os
import sys
import json
import shutil
import platform
from pathlib import Path

# Get the absolute path of the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))

# Get the path to the host manifest
manifest_path = os.path.join(current_dir, 'com.feedbackloop.host.json')

# Get the path to the host script
host_path = os.path.join(current_dir, 'feedbackloop_host.py')

# Make the host script executable
os.chmod(host_path, 0o755)

# Update the host manifest with the absolute path to the host script
with open(manifest_path, 'r') as f:
    manifest = json.load(f)

manifest['path'] = host_path

# Write the updated manifest
with open(manifest_path, 'w') as f:
    json.dump(manifest, f, indent=2)

# Determine the target directory based on the operating system
def get_target_dir():
    system = platform.system()
    if system == 'Darwin':  # macOS
        return os.path.join(str(Path.home()), 'Library', 'Application Support', 'Google', 'Chrome', 'NativeMessagingHosts')
    elif system == 'Linux':
        return os.path.join(str(Path.home()), '.config', 'google-chrome', 'NativeMessagingHosts')
    elif system == 'Windows':
        # On Windows, the registry is used instead
        # This is a simplified version - in reality, you'd need to modify the registry
        return os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data', 'NativeMessagingHosts')
    else:
        print(f"Unsupported operating system: {system}")
        sys.exit(1)

# Create the target directory if it doesn't exist
target_dir = get_target_dir()
os.makedirs(target_dir, exist_ok=True)

# Copy the manifest to the target directory
target_manifest_path = os.path.join(target_dir, 'com.feedbackloop.host.json')
shutil.copy2(manifest_path, target_manifest_path)

print(f"Native messaging host installed to: {target_dir}")
print("Installation complete!")

# Create the .feedbackloop directory in the user's home directory
feedback_dir = os.path.join(str(Path.home()), '.feedbackloop')
os.makedirs(feedback_dir, exist_ok=True)

# Create an empty feedback.log file
feedback_log = os.path.join(feedback_dir, 'feedback.log')
if not os.path.exists(feedback_log):
    with open(feedback_log, 'w') as f:
        f.write("# FeedbackLoop Log File\n")

print(f"Created feedback log file at: {feedback_log}")
print("You can now use the FeedbackLoop extension!")

# Additional instructions for Windows
if platform.system() == 'Windows':
    print("\nOn Windows, you also need to add a registry key. Run the following command in an Administrator command prompt:")
    print(f'REG ADD "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\NativeMessagingHosts\\com.feedbackloop.host" /ve /t REG_SZ /d "{target_manifest_path}" /f') 