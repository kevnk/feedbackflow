#!/usr/bin/env python3
import os
import sys
import time
import shutil
import argparse
import subprocess
import platform
from pathlib import Path

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
            [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Feedback Flow').Show($toast)
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

def detect_ide():
    """
    Detect which IDE's terminal we're running in.
    Returns a tuple of (ide_name, editor_command)
    """
    # Check environment variables to detect the IDE
    env_vars = os.environ
    
    # Debug: Print all environment variables to help diagnose
    # print("Environment variables:")
    # for key, value in env_vars.items():
    #     print(f"{key}={value}")
    
    # Check for Cursor-specific environment variables
    if 'CURSOR_APP_PATH' in env_vars or 'CURSOR_TERMINAL' in env_vars:
        return 'Cursor', 'cursor'
    
    # Check if we're running from Cursor's task runner
    # Cursor's task runner appears to use VS Code's task runner under the hood
    if 'VSCODE_CLI' in env_vars or 'VSCODE_PID' in env_vars or 'VSCODE_IPC_HOOK' in env_vars:
        # If we're in Cursor but the task runner is using VS Code's infrastructure,
        # we should still try to use Cursor first
        try:
            # Check if cursor is available
            subprocess.run(['cursor', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            return 'Cursor', 'cursor'
        except FileNotFoundError:
            # Fall back to VS Code if Cursor command is not available
            return 'VS Code', 'code'
    
    # Check for Spyder
    if any('SPYDER' in name for name in env_vars) or any('SPY_' in name for name in env_vars):
        return 'Spyder', None  # Spyder doesn't have a simple command-line opener
    
    # Check for PyCharm
    if any(var in env_vars for var in ['PYCHARM_HOSTED', 'JETBRAINS_IDE', '_INTELLIJ_COMMAND_HISTFILE_']):
        return 'PyCharm', None  # PyCharm doesn't have a simple command-line opener
    
    # Check for IDLE
    if 'IDLE_CONSOLE' in env_vars or 'pythonw.exe' in sys.executable:
        return 'IDLE', None
    
    # Check for Atom
    if 'ATOM_HOME' in env_vars or 'ATOM_SHELL_INTERNAL_RUN_AS_NODE' in env_vars:
        return 'Atom', 'atom'
    
    # Check for Sublime Text (harder to detect)
    # No reliable environment variable, so we'll check if it's installed
    try:
        if platform.system() == 'Darwin':  # macOS
            if os.path.exists('/Applications/Sublime Text.app'):
                return 'Sublime Text', 'subl'
        elif platform.system() == 'Windows':
            # Check common installation paths
            program_files = os.environ.get('ProgramFiles', 'C:\\Program Files')
            if os.path.exists(os.path.join(program_files, 'Sublime Text 3')):
                return 'Sublime Text', 'subl'
        # For Linux, we'd need to check multiple locations
    except Exception:
        pass
    
    # Check for terminal type
    if 'TERM_PROGRAM' in env_vars:
        term_program = env_vars['TERM_PROGRAM']
        if term_program == 'vscode':
            # If we're in VS Code's terminal, try to use Cursor first if available
            try:
                subprocess.run(['cursor', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                return 'Cursor', 'cursor'
            except FileNotFoundError:
                return 'VS Code Terminal', 'code'
        elif term_program == 'iTerm.app':
            return 'iTerm', None
        elif term_program == 'Apple_Terminal':
            return 'Terminal.app', None
        else:
            return f'{term_program} Terminal', None
    
    # If we've reached here, try to detect if Cursor is available
    try:
        subprocess.run(['cursor', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        return 'Cursor', 'cursor'
    except FileNotFoundError:
        pass
    
    # No IDE detected, return None
    return None, None

def open_with_system_default(file_path):
    """Open a file with the system's default application"""
    try:
        if platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', file_path])
            return True
        elif platform.system() == 'Windows':
            os.startfile(file_path)
            return True
        else:  # Linux
            subprocess.run(['xdg-open', file_path])
            return True
    except Exception as e:
        print(f"Error opening file with system default: {e}")
        return False

def add_feedback_to_composer(editor=None):
    """
    Copy the feedback.log file to a temporary file in the workspace and open it in the editor.
    This makes it easy to add the feedback log to the Composer context.
    
    Args:
        editor (str, optional): Explicitly specify which editor to use ('cursor', 'vscode', 'system').
                               If None, auto-detection will be used.
    """
    # Get the home directory
    home_dir = str(Path.home())
    
    # Get the path to the feedback log file
    log_path = os.path.join(home_dir, '.feedbackflow', 'feedback.log')
    
    # Check if the file exists
    if not os.path.exists(log_path):
        print(f"Feedback log file not found at: {log_path}")
        print("Make sure the Feedback Flow extension is installed and has been used.")
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
                "Feedback Flow",
                "Feedback log content has been copied to your clipboard!"
            )
    except Exception as e:
        print(f"Error copying to clipboard: {e}")
    
    # Open the file in the editor
    try:
        # If editor is explicitly specified, use it
        if editor:
            if editor.lower() == 'cursor':
                ide_name, editor_cmd = 'Cursor', 'cursor'
            elif editor.lower() in ['vscode', 'code']:
                ide_name, editor_cmd = 'VS Code', 'code'
            elif editor.lower() == 'system':
                ide_name, editor_cmd = 'System Default', None
            else:
                # Try to use the specified editor directly
                ide_name, editor_cmd = f'Custom ({editor})', editor
        else:
            # Auto-detect the IDE
            ide_name, editor_cmd = detect_ide()
        
        if ide_name and editor_cmd:
            print(f"Using {ide_name} to open feedback log...")
            try:
                cmd = [editor_cmd, '-r', temp_file_path]
                subprocess.run(cmd)
                print(f"\nFeedback log has been opened in {ide_name}.")
            except FileNotFoundError:
                print(f"Could not open with {ide_name}. Trying system default...")
                if open_with_system_default(temp_file_path):
                    print("\nFeedback log has been opened with the system's default text editor.")
        else:
            # No IDE detected or no command available, use system default
            print("Opening with system default...")
            if open_with_system_default(temp_file_path):
                print("\nFeedback log has been opened with the system's default text editor.")
            else:
                print("Could not open the file. Please open it manually.")
                print(f"File location: {temp_file_path}")
        
        print("\nTo add it to the Composer context:")
        print("1. EASIEST: Paste the content directly into the Composer (it's already in your clipboard)")
        print("2. Drag and drop the file from the Explorer into the Composer")
        print("3. Right-click on the file in the Explorer and select 'Add to Composer' (if available)")
            
    except Exception as e:
        print(f"Error opening file in editor: {e}")

def watch_and_add_feedback(editor=None):
    """
    Watch the feedback log file for changes and automatically add it to the composer when changes are detected.
    
    Args:
        editor (str, optional): Explicitly specify which editor to use ('cursor', 'vscode', 'system').
                               If None, auto-detection will be used.
    """
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
    print("When changes are detected, feedback will be automatically added to the composer.")
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
                    print("\nNew feedback detected:")
                    print(new_content, end='')
                
                # Update the last size
                last_size = current_size
                
                # Add the feedback to the composer
                print("\nAdding feedback to composer...")
                add_feedback_to_composer(editor=editor)
            
            # Sleep for a short time
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopped watching the feedback log file.")

def main():
    """Parse command-line arguments and run the script."""
    parser = argparse.ArgumentParser(description='Watch for feedback and add to composer when detected.')
    parser.add_argument('--editor', '-e', choices=['cursor', 'vscode', 'system'], 
                        help='Explicitly specify which editor to use')
    
    args = parser.parse_args()
    watch_and_add_feedback(editor=args.editor)

if __name__ == '__main__':
    main() 