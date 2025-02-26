#!/usr/bin/env python3
import sys
import json
import struct
import os
import time
from pathlib import Path

# Function to get message from Chrome
def get_message():
    # Read the message length (first 4 bytes)
    text_length_bytes = sys.stdin.buffer.read(4)
    if len(text_length_bytes) == 0:
        sys.exit(0)
    
    # Unpack message length as 4-byte little-endian unsigned int
    text_length = struct.unpack('=I', text_length_bytes)[0]
    
    # Read the JSON message
    text = sys.stdin.buffer.read(text_length).decode('utf-8')
    return json.loads(text)

# Function to send a message to Chrome
def send_message(message):
    # Encode the message as JSON
    encoded_message = json.dumps(message).encode('utf-8')
    
    # Write the message size as a 4-byte little-endian unsigned int
    sys.stdout.buffer.write(struct.pack('=I', len(encoded_message)))
    
    # Write the message itself
    sys.stdout.buffer.write(encoded_message)
    sys.stdout.buffer.flush()

# Main function
def main():
    # Get the home directory
    home_dir = str(Path.home())
    
    # Create the .feedbackloop directory if it doesn't exist
    feedback_dir = os.path.join(home_dir, '.feedbackloop')
    os.makedirs(feedback_dir, exist_ok=True)
    
    # Process messages from Chrome
    while True:
        try:
            message = get_message()
            
            if message.get('action') == 'writeFeedback':
                # Get the log file path
                log_path = os.path.join(home_dir, message.get('path', '.feedbackloop/feedback.log'))
                
                # Ensure the directory exists
                os.makedirs(os.path.dirname(log_path), exist_ok=True)
                
                # Write to the log file
                with open(log_path, 'a', encoding='utf-8') as f:
                    f.write(message.get('content', ''))
                
                # Send success response
                send_message({'success': True})
            elif message.get('action') == 'clearFeedback':
                # Get the log file path
                log_path = os.path.join(home_dir, message.get('path', '.feedbackloop/feedback.log'))
                
                # Clear the log file by opening it in write mode
                with open(log_path, 'w', encoding='utf-8') as f:
                    f.write("# FeedbackLoop Log File - Cleared on " + time.strftime('%Y-%m-%d %H:%M:%S') + "\n")
                
                # Send success response
                send_message({'success': True})
            else:
                # Send error for unknown action
                send_message({'success': False, 'error': 'Unknown action'})
                
        except Exception as e:
            # Send error message
            send_message({'success': False, 'error': str(e)})
            # Log the error
            with open(os.path.join(feedback_dir, 'error.log'), 'a') as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Error: {str(e)}\n")

if __name__ == '__main__':
    main() 