"""
Setup script for testing the image generation system
Creates necessary directories and sample templates
"""

import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_test_environment():
    """Create directories and sample templates for testing"""
    
    # Create directories
    directories = ["templates", "fonts", "output", "test_output"]
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"Created directory: {dir_name}")
    
    # Create sample templates
    create_sample_templates()
    
    # Download or create sample font
    create_sample_font_info()
    
    print("\nTest environment setup complete!")
    print("Run: python image_generator.py to test")

def create_sample_templates():
    """Create sample template backgrounds"""
    
    # Professional news post template
    create_news_post_template()
    
    # Quote-focused template
    create_quote_post_template()
    
    # Backward compatibility
    create_quote_template()
    create_longform_template()

def create_news_post_template():
    """Create professional news post template"""
    img = Image.new("RGBA", (1080, 1080), color="#000000")
    draw = ImageDraw.Draw(img)
    
    # Header section with branding
    draw.rectangle([0, 0, 1080, 140], fill="#111111")
    draw.rectangle([0, 135, 1080, 140], fill="#00ff00")
    
    # Logo area (top right)
    draw.rectangle([850, 20, 1050, 100], outline="#00ff00", width=2)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    draw.text((870, 50), "the based", fill="#ffffff", font=font)
    draw.text((870, 75), "labs", fill="#00ff00", font=font)
    
    # Main content area background
    draw.rectangle([60, 160, 1020, 860], fill="#0a0a0a", outline="#333333", width=1)
    
    # Side accent lines
    draw.rectangle([0, 180, 8, 840], fill="#00ff00")
    draw.rectangle([1072, 180, 1080, 840], fill="#00ff00")
    
    # Footer area
    draw.rectangle([0, 940, 1080, 1080], fill="#111111")
    
    # Social handle
    try:
        small_font = ImageFont.truetype("arial.ttf", 18)
    except:
        small_font = ImageFont.load_default()
    draw.text((80, 1000), "@thebasedlabs", fill="#888888", font=small_font)
    
    # Subtle pattern in background
    for i in range(100, 1000, 120):
        for j in range(200, 800, 120):
            draw.ellipse([i, j, i+2, j+2], fill="#222222")
    
    img.save("templates/news_post_bg.png")
    print("Created: templates/news_post_bg.png")

def create_quote_post_template():
    """Create quote-focused template"""
    img = Image.new("RGBA", (1080, 1080), color="#000000")
    draw = ImageDraw.Draw(img)
    
    # Minimal header
    draw.rectangle([0, 0, 1080, 80], fill="#111111")
    draw.rectangle([0, 75, 1080, 80], fill="#00ff00")
    
    # Logo (smaller, top right)
    draw.rectangle([900, 15, 1060, 65], outline="#00ff00", width=1)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    draw.text((920, 35), "BASED LABS", fill="#00ff00", font=font)
    
    # Central focus area for quote
    draw.rectangle([40, 150, 1040, 750], outline="#333333", width=1)
    
    # Accent elements for visual interest
    draw.rectangle([0, 400, 15, 680], fill="#00ff00")
    draw.rectangle([1065, 400, 1080, 680], fill="#00ff00")
    
    # Bottom branding
    draw.rectangle([0, 1000, 1080, 1080], fill="#111111")
    
    # Handle
    try:
        small_font = ImageFont.truetype("arial.ttf", 18)
    except:
        small_font = ImageFont.load_default()
    draw.text((80, 1030), "@thebasedlabs", fill="#888888", font=small_font)
    
    # Geometric accent
    draw.polygon([(540, 100), (560, 120), (540, 140), (520, 120)], fill="#00ff00")
    
    img.save("templates/quote_post_bg.png")
    print("Created: templates/quote_post_bg.png")

def create_quote_template():
    """Backward compatibility - calls new quote template"""
    create_quote_post_template()

def create_longform_template():
    """Backward compatibility - calls new news template"""  
    create_news_post_template()

def create_sample_font_info():
    """Provide instructions for font setup"""
    font_info = """
Font Setup Instructions:
========================

For best results, download Inter font:
1. Go to: https://fonts.google.com/specimen/Inter
2. Download Inter font family
3. Copy Inter-Bold.ttf to the 'fonts/' directory

Alternative: The system will fallback to system fonts if Inter is not available.

For macOS: System fonts like Arial will be used
For Linux: Install fonts-liberation package
For Windows: Arial/Calibri will be used as fallback
"""
    
    with open("fonts/README.txt", "w") as f:
        f.write(font_info)
    
    print("Created: fonts/README.txt with setup instructions")

if __name__ == "__main__":
    create_test_environment()