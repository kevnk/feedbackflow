#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path
import subprocess
import platform

def copy_to_clipboard(text):
    """Copy text to clipboard using platform-specific methods"""
    try:
        # Try using platform-specific commands
        if platform.system() == 'Darwin':  # macOS
            process = subprocess.Popen(
                'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            return True
        elif platform.system() == 'Windows':
            process = subprocess.Popen(
                'clip', stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            return True
        else:  # Linux
            # Try xclip (X11)
            try:
                process = subprocess.Popen(
                    ['xclip', '-selection', 'clipboard'],
                    stdin=subprocess.PIPE)
                process.communicate(text.encode('utf-8'))
                return True
            except FileNotFoundError:
                # Try xsel (X11)
                try:
                    process = subprocess.Popen(
                        ['xsel', '--clipboard', '--input'],
                        stdin=subprocess.PIPE)
                    process.communicate(text.encode('utf-8'))
                    return True
                except FileNotFoundError:
                    # Try wl-copy (Wayland)
                    try:
                        process = subprocess.Popen(
                            ['wl-copy'],
                            stdin=subprocess.PIPE)
                        process.communicate(text.encode('utf-8'))
                        return True
                    except FileNotFoundError:
                        print("Could not find clipboard command. Content not copied to clipboard.")
                        return False
    except Exception as e:
        print(f"Error copying to clipboard: {e}")
        return False

def show_notification(title, message):
    """Show a notification using platform-specific methods"""
    try:
        if platform.system() == 'Darwin':  # macOS
            os.system(f"""
                osascript -e 'display notification "{message}" with title "{title}"'
            """)
        elif platform.system() == 'Windows':
            # Using PowerShell for Windows notifications
            powershell_cmd = f"""
            powershell -Command "
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
            [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
            $template = [Windows.UI.Notifications.ToastTemplateType]::ToastText02
            $xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent($template)
            $text = $xml.GetElementsByTagName('text')
            $text[0].AppendChild($xml.CreateTextNode('{title}'))
            $text[1].AppendChild($xml.CreateTextNode('{message}'))
            $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
            [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('FeedbackLoop').Show($toast)
            "
            """
            subprocess.run(powershell_cmd, shell=True)
        else:  # Linux
            # Try using notify-send
            try:
                subprocess.run(['notify-send', title, message])
            except FileNotFoundError:
                print(f"{title}: {message}")
    except Exception as e:
        print(f"Error showing notification: {e}")
        print(f"{title}: {message}")

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
    
    # Read the content of the feedback log
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            feedback_content = f.read()
            
        # Copy the content to the clipboard
        if copy_to_clipboard(feedback_content):
            print("Feedback log content copied to clipboard!")
            print("You can now paste it directly into the Composer.")
            
            # Show a notification
            show_notification(
                "FeedbackLoop",
                "Feedback log content has been copied to your clipboard!"
            )
    except Exception as e:
        print(f"Error copying to clipboard: {e}")
    
    # Open the file in the editor
    try:
        # Determine the command to open the file based on the platform
        if platform.system() == 'Darwin':  # macOS
            # Try to use Cursor first, fall back to code if cursor is not available
            try:
                cmd = ['cursor', '-r', temp_file_path]
                subprocess.run(cmd)
            except FileNotFoundError:
                # Fall back to VS Code if Cursor is not available
                cmd = ['code', '-r', temp_file_path]
                subprocess.run(cmd)
        elif platform.system() == 'Windows':
            # Try to use Cursor first, fall back to code if cursor is not available
            try:
                cmd = ['cursor', '-r', temp_file_path]
                subprocess.run(cmd)
            except FileNotFoundError:
                # Fall back to VS Code if Cursor is not available
                cmd = ['code', '-r', temp_file_path]
                subprocess.run(cmd)
        else:  # Linux
            # Try to use Cursor first, fall back to code if cursor is not available
            try:
                cmd = ['cursor', '-r', temp_file_path]
                subprocess.run(cmd)
            except FileNotFoundError:
                # Fall back to VS Code if Cursor is not available
                cmd = ['code', '-r', temp_file_path]
                subprocess.run(cmd)
        
        print("\nFeedback log has been opened in the editor.")
        print("\nTo add it to the Cursor composer context:")
        print("1. EASIEST: Paste the content directly into the Composer (it's already in your clipboard)")
        print("2. Drag and drop the file from the Explorer into the Composer")
        print("3. Right-click on the file in the Explorer and select 'Add to Composer' (if available)")
            
    except Exception as e:
        print(f"Error opening file in editor: {e}")

if __name__ == '__main__':
    add_feedback_to_composer() 