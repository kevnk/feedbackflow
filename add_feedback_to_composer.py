#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path
import subprocess
import platform

def add_feedback_to_composer():
    """
    Copy the feedback.log file to a temporary file in the workspace and open it in the editor.
    This makes it easy to add the feedback log to the Cursor composer context.
    """
    # Get the home directory
    home_dir = str(Path.home())
    
    # Get the path to the feedback log file
    log_path = os.path.join(home_dir, '.feedbackloop', 'feedback.log')
    
    # Check if the file exists
    if not os.path.exists(log_path):
        print(f"Feedback log file not found at: {log_path}")
        print("Make sure the FeedbackLoop extension is installed and has been used.")
        return
    
    # Get the current workspace directory
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create a temporary file in the workspace
    temp_file_path = os.path.join(workspace_dir, 'feedback_log_for_composer.txt')
    
    # Copy the feedback log to the temporary file
    try:
        shutil.copy2(log_path, temp_file_path)
        print(f"Copied feedback log to: {temp_file_path}")
    except Exception as e:
        print(f"Error copying feedback log: {e}")
        return
    
    # Open the file in the editor
    try:
        # Determine the command to open the file based on the platform
        if platform.system() == 'Darwin':  # macOS
            cmd = ['code', '-r', temp_file_path]
        elif platform.system() == 'Windows':
            cmd = ['code', '-r', temp_file_path]
        else:  # Linux
            cmd = ['code', '-r', temp_file_path]
        
        subprocess.run(cmd)
        
        print("\nFeedback log has been opened in the editor.")
        print("\nTo add it to the Cursor composer context:")
        print("1. Drag and drop the file from the Explorer into the Composer")
        print("   OR")
        print("2. Right-click on the file in the Explorer and select 'Add to Composer' (if available)")
        print("   OR")
        print("3. Copy the contents and paste them into the Composer")
    except Exception as e:
        print(f"Error opening file in editor: {e}")

if __name__ == '__main__':
    add_feedback_to_composer() 