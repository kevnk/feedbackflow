#!/usr/bin/env python3
import os
from PIL import Image

def create_icon(size, output_dir="images", source_image="public/ff-icon.png"):
    """Create icon of the specified size from the source image."""
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Open the source image
    try:
        img = Image.open(source_image)
        # Resize the image to the required size
        img = img.resize((size, size), Image.LANCZOS)
        
        # Save the image
        output_path = os.path.join(output_dir, f"icon{size}.png")
        img.save(output_path)
        print(f"Created {output_path}")
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    # Create icons of different sizes
    create_icon(16)
    create_icon(48)
    create_icon(128)
    
    print("\nIcons created successfully in the 'images' directory.")
    print("The icons were created from the source image: public/ff-icon.png") 