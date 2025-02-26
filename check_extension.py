#!/usr/bin/env python3
import os
import sys
import platform
from pathlib import Path

def check_log_file():
    """Check if the feedback log file exists and is accessible."""
    # Get the home directory
    home_dir = str(Path.home())
    
    # Get the path to the feedback log file
    log_path = os.path.join(home_dir, '.feedbackloop', 'feedback.log')
    
    # Check if the file exists
    if not os.path.exists(log_path):
        print(f"❌ Feedback log file not found at: {log_path}")
        print("   Make sure the native host is installed correctly.")
        return False
    
    # Check if the file is readable
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ Feedback log file found and readable at: {log_path}")
        return True
    except Exception as e:
        print(f"❌ Error reading feedback log file: {e}")
        return False

def check_native_host():
    """Check if the native messaging host is installed correctly."""
    system = platform.system()
    
    if system == 'Darwin':  # macOS
        host_dir = os.path.join(str(Path.home()), 'Library', 'Application Support', 'Google', 'Chrome', 'NativeMessagingHosts')
        manifest_path = os.path.join(host_dir, 'com.feedbackloop.host.json')
    elif system == 'Linux':
        host_dir = os.path.join(str(Path.home()), '.config', 'google-chrome', 'NativeMessagingHosts')
        manifest_path = os.path.join(host_dir, 'com.feedbackloop.host.json')
    elif system == 'Windows':
        # On Windows, we can't easily check the registry, so we'll just check if the directory exists
        host_dir = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data', 'NativeMessagingHosts')
        manifest_path = os.path.join(host_dir, 'com.feedbackloop.host.json')
    else:
        print(f"❌ Unsupported operating system: {system}")
        return False
    
    # Check if the directory exists
    if not os.path.exists(host_dir):
        print(f"❌ Native messaging host directory not found at: {host_dir}")
        return False
    
    # Check if the manifest file exists
    if not os.path.exists(manifest_path):
        print(f"❌ Native messaging host manifest not found at: {manifest_path}")
        return False
    
    print(f"✅ Native messaging host appears to be installed correctly.")
    return True

def main():
    """Main function to check if the extension is working correctly."""
    print("=== FeedbackLoop Extension Check ===\n")
    
    # Check if the native host is installed
    native_host_ok = check_native_host()
    
    # Check if the log file exists
    log_file_ok = check_log_file()
    
    # Print summary
    print("\n=== Summary ===")
    if native_host_ok and log_file_ok:
        print("✅ The FeedbackLoop extension appears to be set up correctly.")
        print("   You can now use the extension to send feedback from your browser.")
    else:
        print("❌ There are issues with the FeedbackLoop extension setup.")
        print("   Please check the errors above and try running the setup script again:")
        print("   python setup.py")
    
    print("\nTo test the extension:")
    print("1. Make sure the extension is loaded in Chrome")
    print("2. Run the sample website: python -m http.server 8000 (in the sample-website directory)")
    print("3. Open http://localhost:8000 in Chrome")
    print("4. Try sending feedback using the form on the page")
    print("5. Check if the feedback appears in the log file: python read_feedback.py")

if __name__ == "__main__":
    main() 