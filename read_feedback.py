#!/usr/bin/env python3
import os
import sys
import time
from pathlib import Path

def read_feedback_log():
    """Read the feedback log file and print its contents."""
    # Get the home directory
    home_dir = str(Path.home())
    
    # Get the path to the feedback log file
    log_path = os.path.join(home_dir, '.feedbackflow', 'feedback.log')
    
    # Check if the file exists
    if not os.path.exists(log_path):
        print(f"Feedback log file not found at: {log_path}")
        print("Make sure the Feedback Flow extension is installed and has been used.")
        return
    
    # Read and print the contents of the log file
    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)

def watch_feedback_log():
    """Watch the feedback log file for changes and print new entries."""
    # Get the home directory
    home_dir = str(Path.home())
    
    # Get the path to the feedback log file
    log_path = os.path.join(home_dir, '.feedbackflow', 'feedback.log')
    
    # Check if the file exists
    if not os.path.exists(log_path):
        print(f"Feedback log file not found at: {log_path}")
        print("Make sure the Feedback Flow extension is installed and has been used.")
        return
    
    # Get the current size of the file
    last_size = os.path.getsize(log_path)
    
    print(f"Watching feedback log file at: {log_path}")
    print("Press Ctrl+C to stop watching.")
    
    try:
        while True:
            # Check if the file size has changed
            current_size = os.path.getsize(log_path)
            
            if current_size > last_size:
                # Read only the new content
                with open(log_path, 'r', encoding='utf-8') as f:
                    f.seek(last_size)
                    new_content = f.read()
                    print(new_content, end='')
                
                # Update the last size
                last_size = current_size
            
            # Sleep for a short time
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopped watching the feedback log file.")

if __name__ == '__main__':
    # Check if the user wants to watch the log file
    if len(sys.argv) > 1 and sys.argv[1] == '--watch':
        watch_feedback_log()
    else:
        read_feedback_log()
        print("\nTo watch for new feedback entries, run: python read_feedback.py --watch") 