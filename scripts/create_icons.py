#!/usr/bin/env python3
import os
from PIL import Image

def create_icon(size, output_dir="chrome-extension/images", source_image="../public/ff-icon.png"):
    """Create icon of the specified size from the source image."""
    # Get the absolute path of the current directory
    current_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    
    # Create the output directory if it doesn't exist
    output_dir_path = os.path.join(project_root, output_dir)
    os.makedirs(output_dir_path, exist_ok=True)
    
    # Open the source image
    try:
        source_path = os.path.join(project_root, "public/ff-icon.png")
        img = Image.open(source_path)
        # Resize the image to the required size
        img = img.resize((size, size), Image.LANCZOS)
        
        # Save the image
        output_path = os.path.join(output_dir_path, f"icon{size}.png")
        img.save(output_path)
        print(f"Created {output_path}")
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    # Create icons of different sizes
    create_icon(16)
    create_icon(48)
    create_icon(128)
    
    print("\nIcons created successfully in the 'chrome-extension/images' directory.")
    print("The icons were created from the source image: public/ff-icon.png") 