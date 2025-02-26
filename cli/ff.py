#!/usr/bin/env python3

import os
import sys
import json
import shutil
import argparse
import re

def create_ai_assistant_files(target_dir):
    """
    Create or update AI assistant integration files for FeedbackFlow in the target directory.
    
    Args:
        target_dir (str): The target directory where to add the AI assistant files
    """
    print(f"Adding FeedbackFlow AI assistant integration files to: {target_dir}")
    
    # Ensure target directory exists
    if not os.path.isdir(target_dir):
        print(f"Error: {target_dir} is not a valid directory")
        sys.exit(1)
    
    # Get absolute path of target directory
    target_dir = os.path.abspath(target_dir)
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Paths to template files
    cursorrules_template_path = os.path.join(script_dir, "user_cursorrules_template.json")
    copilot_template_path = os.path.join(script_dir, "user_copilot_instructions_template.md")
    
    # Check if template files exist
    if not os.path.exists(cursorrules_template_path):
        print(f"Error: Template file {cursorrules_template_path} not found")
        sys.exit(1)
    
    if not os.path.exists(copilot_template_path):
        print(f"Error: Template file {copilot_template_path} not found")
        sys.exit(1)
    
    # Install .cursorrules
    try:
        # Read the template file
        with open(cursorrules_template_path, "r") as f:
            cursorrules_content = json.load(f)
        
        # Get user's home directory
        home_dir = os.path.expanduser("~")
        
        # Write to user's .cursorrules file
        user_cursorrules_path = os.path.join(home_dir, ".cursorrules")
        
        # If .cursorrules already exists, merge with existing content
        if os.path.exists(user_cursorrules_path):
            try:
                with open(user_cursorrules_path, "r") as f:
                    existing_content = json.load(f)
                
                # Add FeedbackFlow section to existing rules
                if "projectRules" in existing_content:
                    existing_content["projectRules"]["feedbackFlow"] = cursorrules_content["projectRules"]["feedbackFlow"]
                else:
                    existing_content["projectRules"] = {"feedbackFlow": cursorrules_content["projectRules"]["feedbackFlow"]}
                
                with open(user_cursorrules_path, "w") as f:
                    json.dump(existing_content, f, indent=2)
                
                print(f"✅ Updated existing .cursorrules file at {user_cursorrules_path}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error updating existing .cursorrules: {e}")
                print("Creating a backup and writing new .cursorrules file...")
                
                # Create backup of existing file
                backup_path = os.path.join(home_dir, ".cursorrules.backup")
                shutil.copy2(user_cursorrules_path, backup_path)
                print(f"Backup created at {backup_path}")
                
                # Write new file
                with open(user_cursorrules_path, "w") as f:
                    json.dump(cursorrules_content, f, indent=2)
                print(f"✅ Created new .cursorrules file at {user_cursorrules_path}")
        else:
            # Write new file
            with open(user_cursorrules_path, "w") as f:
                json.dump(cursorrules_content, f, indent=2)
            print(f"✅ Created .cursorrules file at {user_cursorrules_path}")
    except Exception as e:
        print(f"❌ Error installing .cursorrules: {e}")
    
    # Install .github/copilot-instructions.md
    try:
        # Create .github directory if it doesn't exist
        github_dir = os.path.join(target_dir, ".github")
        if not os.path.exists(github_dir):
            os.makedirs(github_dir)
        
        # Path to the target copilot-instructions.md file
        copilot_path = os.path.join(github_dir, "copilot-instructions.md")
        
        # Read the template file
        with open(copilot_template_path, "r") as f:
            copilot_content = f.read()
        
        # Check if copilot-instructions.md already exists
        if os.path.exists(copilot_path):
            print(f"Found existing copilot-instructions.md at {copilot_path}")
            
            # Read existing content
            with open(copilot_path, "r") as f:
                existing_content = f.read()
            
            # Create backup of existing file
            backup_path = os.path.join(github_dir, "copilot-instructions.md.backup")
            with open(backup_path, "w") as f:
                f.write(existing_content)
            print(f"Backup created at {backup_path}")
            
            # Check if FeedbackFlow section already exists
            if "FeedbackFlow Integration" in existing_content:
                print("FeedbackFlow section already exists in copilot-instructions.md")
                print("Updating the existing section...")
                
                # Extract the FeedbackFlow section from the template
                feedbackflow_section = extract_feedbackflow_section(copilot_content)
                
                # Replace the existing FeedbackFlow section or append if pattern doesn't match
                pattern = r"# FeedbackFlow Integration.*?(?=# |$)"
                if re.search(pattern, existing_content, re.DOTALL):
                    updated_content = re.sub(pattern, feedbackflow_section, existing_content, flags=re.DOTALL)
                else:
                    updated_content = existing_content + "\n\n" + feedbackflow_section
            else:
                # Append FeedbackFlow section to existing content
                updated_content = existing_content + "\n\n" + copilot_content
            
            # Write updated content
            with open(copilot_path, "w") as f:
                f.write(updated_content)
            
            print(f"✅ Updated GitHub Copilot instructions at {copilot_path}")
        else:
            # Write new file
            with open(copilot_path, "w") as f:
                f.write(copilot_content)
            
            print(f"✅ Created GitHub Copilot instructions at {copilot_path}")
    except Exception as e:
        print(f"❌ Error installing GitHub Copilot instructions: {e}")
    
    # Check for project-specific .cursorrules
    try:
        project_cursorrules_path = os.path.join(target_dir, ".cursorrules")
        
        if os.path.exists(project_cursorrules_path):
            print(f"Found project-specific .cursorrules at {project_cursorrules_path}")
            
            try:
                # Read existing content
                with open(project_cursorrules_path, "r") as f:
                    existing_content = json.load(f)
                
                # Create backup of existing file
                backup_path = os.path.join(target_dir, ".cursorrules.backup")
                with open(backup_path, "w") as f:
                    json.dump(existing_content, f, indent=2)
                print(f"Backup created at {backup_path}")
                
                # Add FeedbackFlow section to existing rules
                if "projectRules" in existing_content:
                    existing_content["projectRules"]["feedbackFlow"] = cursorrules_content["projectRules"]["feedbackFlow"]
                else:
                    existing_content["projectRules"] = {"feedbackFlow": cursorrules_content["projectRules"]["feedbackFlow"]}
                
                # Write updated content
                with open(project_cursorrules_path, "w") as f:
                    json.dump(existing_content, f, indent=2)
                
                print(f"✅ Updated project-specific .cursorrules at {project_cursorrules_path}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error updating project-specific .cursorrules: {e}")
                print("Creating a backup and writing new content...")
                
                # Create backup of existing file
                backup_path = os.path.join(target_dir, ".cursorrules.backup")
                shutil.copy2(project_cursorrules_path, backup_path)
                print(f"Backup created at {backup_path}")
                
                # Write new file
                with open(project_cursorrules_path, "w") as f:
                    json.dump(cursorrules_content, f, indent=2)
                print(f"✅ Created new project-specific .cursorrules at {project_cursorrules_path}")
    except Exception as e:
        print(f"❌ Error handling project-specific .cursorrules: {e}")
    
    print("\n🎉 FeedbackFlow AI assistant integration complete!")
    print("\nThese files will help AI assistants understand how to use FeedbackFlow in your projects.")
    print("\nYou can now use FeedbackFlow in your project with the help of AI assistants.")
    print("For example, ask Cursor AI or GitHub Copilot to 'add a feedback button to my website'.")

def extract_feedbackflow_section(content):
    """Extract the FeedbackFlow section from the content."""
    pattern = r"# FeedbackFlow Integration.*?(?=# |$)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(0)
    return content  # Return the whole content if no match found

def main():
    """Main function to parse arguments and run the tool."""
    parser = argparse.ArgumentParser(
        description="Add FeedbackFlow AI assistant integration files to a project"
    )
    parser.add_argument(
        "directory", 
        nargs="?", 
        default=".", 
        help="Target directory to add AI assistant files (default: current directory)"
    )
    
    args = parser.parse_args()
    create_ai_assistant_files(args.directory)

if __name__ == "__main__":
    main() 