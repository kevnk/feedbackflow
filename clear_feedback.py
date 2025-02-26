#!/usr/bin/env python3
import os
import time
from pathlib import Path

def clear_feedback_log():
    """Clear the feedback log file and add a timestamp header."""
    # Get the home directory
    home_dir = str(Path.home())
    
    # Get the path to the feedback log file
    log_path = os.path.join(home_dir, '.feedbackflow', 'feedback.log')
    
    # Check if the file exists
    if not os.path.exists(log_path):
        print(f"Feedback log file not found at: {log_path}")
        print("Make sure the Feedback Flow extension is installed and has been used.")
        return False
    
    try:
        # Clear the log file by opening it in write mode
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write("# Feedback Flow Log File - Cleared on " + time.strftime('%Y-%m-%d %H:%M:%S') + "\n")
        print(f"Feedback log cleared successfully at: {log_path}")
        return True
    except Exception as e:
        print(f"Error clearing feedback log: {e}")
        return False

if __name__ == '__main__':
    clear_feedback_log() 