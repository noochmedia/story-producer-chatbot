#!/usr/bin/env python3
import os
import subprocess
import sys

def launch_app():
    # Get the absolute path to the application directory
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Command to run the Flask app
    python_path = sys.executable  # Get the current Python interpreter path
    app_command = f'{python_path} app.py'
    
    # For macOS, use the 'open' command to launch a new Terminal window
    terminal_command = f'''
    tell application "Terminal"
        do script "cd {app_dir} && {app_command}"
        activate
    end tell
    '''
    
    # Use osascript to execute the AppleScript
    subprocess.run(['osascript', '-e', terminal_command])
    
if __name__ == '__main__':
    launch_app()