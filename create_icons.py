#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

def create_icon(size, output_dir="images"):
    """Create a simple icon of the specified size."""
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a new image with a blue background
    img = Image.new('RGB', (size, size), color=(66, 133, 244))  # Google blue
    draw = ImageDraw.Draw(img)
    
    # Try to use a built-in font, or fall back to default
    try:
        # Try to get a font - size is approximate, adjust as needed
        font_size = int(size * 0.7)
        try:
            font = ImageFont.truetype("Arial.ttf", font_size)
        except IOError:
            # Fall back to default font
            font = ImageFont.load_default()
        
        # Draw 'F' in the center
        text = "F"
        text_width, text_height = draw.textsize(text, font=font)
        position = ((size - text_width) // 2, (size - text_height) // 2)
        draw.text(position, text, fill=(255, 255, 255), font=font)
    except Exception as e:
        # If there's any error with the font or drawing, create a simpler icon
        # Draw a white 'F' using rectangles
        margin = size // 4
        # Vertical line
        draw.rectangle([(margin, margin), (margin + size//4, size - margin)], fill=(255, 255, 255))
        # Horizontal lines
        draw.rectangle([(margin, margin), (size - margin, margin + size//4)], fill=(255, 255, 255))
        draw.rectangle([(margin, margin + size//2), (size - margin//2, margin + size//2 + size//4)], fill=(255, 255, 255))
    
    # Save the image
    output_path = os.path.join(output_dir, f"icon{size}.png")
    img.save(output_path)
    print(f"Created {output_path}")

if __name__ == "__main__":
    # Create icons of different sizes
    create_icon(16)
    create_icon(48)
    create_icon(128)
    
    print("\nIcons created successfully in the 'images' directory.")
    print("If you want to create custom icons, replace these files with your own designs.") 