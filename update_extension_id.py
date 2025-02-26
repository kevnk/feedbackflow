#!/usr/bin/env python3
import os
import json
import sys
from pathlib import Path

def update_extension_id(extension_id):
    # Path to the native messaging host manifest in Chrome's directory
    chrome_manifest_path = os.path.join(
        str(Path.home()),
        'Library', 'Application Support', 'Google', 'Chrome', 'NativeMessagingHosts',
        'com.feedbackflow.host.json'
    )
    
    # Paths to the native messaging host manifests in the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    project_manifest_path = os.path.join(
        project_dir,
        'native-host', 'com.feedbackflow.host.json'
    )
    project_example_manifest_path = os.path.join(
        project_dir,
        'native-host', 'com.feedbackflow.host.json.example'
    )
    
    # Update all manifests
    for manifest_path in [chrome_manifest_path, project_manifest_path, project_example_manifest_path]:
        if os.path.exists(manifest_path):
            try:
                # Read the manifest
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                
                # Update the allowed_origins
                manifest['allowed_origins'] = [f"chrome-extension://{extension_id}/"]
                
                # Write the updated manifest
                with open(manifest_path, 'w') as f:
                    json.dump(manifest, f, indent=2)
                
                print(f"Updated extension ID in {manifest_path}")
            except Exception as e:
                print(f"Error updating {manifest_path}: {e}")
        else:
            print(f"Manifest file not found: {manifest_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_extension_id.py <extension_id>")
        sys.exit(1)
    
    extension_id = sys.argv[1]
    update_extension_id(extension_id)
    print(f"Extension ID updated to: {extension_id}")
    print("Please reload the extension in Chrome for the changes to take effect.") 