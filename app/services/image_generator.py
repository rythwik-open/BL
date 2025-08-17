"""
Professional Image Generator for Based Labs
Integrated into the automated content pipeline
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from app.models.generated_content import GeneratedContent

# Try to import advanced libraries (graceful fallback)
try:
    from Wand.image import Image as WandImage
    WAND_AVAILABLE = True
except ImportError:
    WAND_AVAILABLE = False
    print("Wand not available - some advanced effects disabled")

try:
    import skia
    SKIA_AVAILABLE = True
except ImportError:
    SKIA_AVAILABLE = False
    print("Skia not available - using PIL for typography")

@dataclass
class TextArea:
    """Configuration for text placement areas"""
    x: int
    y: int
    max_width: int
    max_height: int
    font_size: int
    color: str = "#ffffff"
    alignment: str = "left"  # left, center, right
    text_type: str = "body"  # title, body, caption
    fallback_strategy: str = "shrink_font"  # shrink_font, truncate, wrap

@dataclass
class Template:
    """Template configuration"""
    name: str
    background_path: str
    text_areas: Dict[str, TextArea]
    suitable_for: List[str]  # content types this template works for

class BasedLabsImageGenerator:
    """Professional image generator with Photoshop-level capabilities"""
    
    def __init__(self, templates_dir: str = "templates", fonts_dir: str = "fonts"):
        self.templates_dir = Path(templates_dir)
        self.fonts_dir = Path(fonts_dir)
        self.templates = self._load_templates()
        self.font_cache = {}
        
        # Create directories if they don't exist
        self.templates_dir.mkdir(exist_ok=True)
        self.fonts_dir.mkdir(exist_ok=True)
        
    def _load_templates(self) -> Dict[str, Template]:
        """Load template configurations"""
        templates = {}
        
        # Based Labs professional templates
        templates["quote_minimal"] = Template(
            name="quote_minimal", 
            background_path="quote_minimal_bg.png",
            text_areas={
                "title": TextArea(
                    x=80, y=300, max_width=920, max_height=400,
                    font_size=64, color="#00ff00", alignment="center",
                    text_type="title"
                ),
                "attribution": TextArea(
                    x=80, y=750, max_width=920, max_height=80,
                    font_size=24, color="#888888", alignment="center",
                    text_type="caption"
                )
            },
            suitable_for=["quote", "hook", "minimal"]
        )
        
        templates["long_form"] = Template(
            name="long_form",
            background_path="long_form_bg.png", 
            text_areas={
                "title": TextArea(
                    x=80, y=150, max_width=920, max_height=200,
                    font_size=48, color="#00ff00", alignment="left",
                    text_type="title"
                ),
                "description": TextArea(
                    x=80, y=400, max_width=920, max_height=400,
                    font_size=28, color="#ffffff", alignment="left",
                    text_type="body"
                ),
                "cta": TextArea(
                    x=80, y=850, max_width=600, max_height=80,
                    font_size=24, color="#00ff00", alignment="left",
                    text_type="caption"
                )
            },
            suitable_for=["framework", "explanation", "educational"]
        )
        
        templates["carousel_series"] = Template(
            name="carousel_series",
            background_path="carousel_bg.png",
            text_areas={
                "slide_number": TextArea(
                    x=950, y=50, max_width=100, max_height=50,
                    font_size=20, color="#00ff00", alignment="center",
                    text_type="caption"
                ),
                "title": TextArea(
                    x=80, y=200, max_width=920, max_height=150,
                    font_size=42, color="#00ff00", alignment="left",
                    text_type="title"
                ),
                "content": TextArea(
                    x=80, y=400, max_width=920, max_height=500,
                    font_size=26, color="#ffffff", alignment="left",
                    text_type="body"
                )
            },
            suitable_for=["carousel", "series", "multi_slide"]
        )
        
        return templates
    
    async def generate_image_for_content(self, content: GeneratedContent) -> Image.Image:
        """
        Generate image for a GeneratedContent object
        
        Args:
            content: GeneratedContent model instance
            
        Returns:
            PIL Image object
        """
        # Convert content to format expected by generator
        content_dict = {
            "main_text": content.text,
            "type": content.content_type,
            "platform": content.platform
        }
        
        # Select template based on content type
        template_name = self._map_content_type_to_template(content.content_type)
        
        return self.generate_post(content_dict, template_name)
    
    def _map_content_type_to_template(self, content_type: str) -> str:
        """Map content types to template names"""
        mapping = {
            "quote_minimal": "quote_minimal",
            "long_form": "long_form", 
            "carousel_series": "carousel_series"
        }
        return mapping.get(content_type, "long_form")
    
    def generate_post(self, content: Dict, template_name: Optional[str] = None) -> Image.Image:
        """
        Generate a professional social media post
        
        Args:
            content: Dict with text content and metadata
            template_name: Specific template to use (auto-selected if None)
            
        Returns:
            PIL Image object
        """
        # Auto-select template if not specified
        if not template_name:
            template_name = self._select_template(content)
        
        template = self.templates[template_name]
        
        # Create base image
        img = self._create_base_image(template)
        
        # Apply professional effects
        img = self._apply_professional_effects(img)
        
        # Add text content
        img = self._add_text_content(img, content, template)
        
        return img
    
    def _select_template(self, content: Dict) -> str:
        """Intelligently select template based on content"""
        content_type = content.get("type", "unknown")
        text_length = len(content.get("main_text", ""))
        
        # Based Labs template selection logic
        if content_type == "quote_minimal" or text_length < 100:
            return "quote_minimal"
        elif content_type == "long_form" or (100 <= text_length <= 800):
            return "long_form"
        elif content_type == "carousel_series" or text_length > 800:
            return "carousel_series"
        else:
            return "long_form"  # Default
    
    def _create_base_image(self, template: Template) -> Image.Image:
        """Create base image with template background"""
        bg_path = self.templates_dir / template.background_path
        
        if bg_path.exists():
            return Image.open(bg_path).convert("RGBA")
        else:
            # Create default Based Labs background
            return self._create_default_background()
    
    def _create_default_background(self) -> Image.Image:
        """Create default Based Labs branded background"""
        # Create black background with neon green accents
        img = Image.new("RGBA", (1080, 1080), color="#000000")
        draw = ImageDraw.Draw(img)
        
        # Add subtle grid pattern
        for i in range(0, 1080, 60):
            draw.line([(i, 0), (i, 1080)], fill="#111111", width=1)
            draw.line([(0, i), (1080, i)], fill="#111111", width=1)
        
        # Add neon accent lines
        draw.rectangle([0, 0, 1080, 5], fill="#00ff00")  # Top accent
        draw.rectangle([0, 1075, 1080, 1080], fill="#00ff00")  # Bottom accent
        
        # Add Based Labs logo area (placeholder)
        draw.rectangle([900, 50, 1030, 120], outline="#00ff00", width=2)
        
        return img
    
    def _apply_professional_effects(self, img: Image.Image) -> Image.Image:
        """Apply Photoshop-level effects to the image"""
        if not WAND_AVAILABLE:
            return img
        
        # Convert PIL to numpy for OpenCV processing
        img_array = np.array(img)
        
        # Professional color grading
        img_array = self._apply_color_grading(img_array)
        
        # Advanced effects with ImageMagick
        img_array = self._apply_wand_effects(img_array)
        
        return Image.fromarray(img_array)
    
    def _apply_color_grading(self, img_array: np.ndarray) -> np.ndarray:
        """Professional color grading using OpenCV"""
        # Convert to different color spaces for professional editing
        if len(img_array.shape) == 3 and img_array.shape[2] == 4:
            # Handle RGBA
            rgb = img_array[:, :, :3]
            alpha = img_array[:, :, 3]
            
            # Apply grading to RGB channels
            lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            
            # Enhance contrast in L channel
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            
            # Subtle color adjustments
            a = cv2.add(a, 2)  # Slight green shift
            
            # Merge back
            lab = cv2.merge([l, a, b])
            rgb = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
            
            # Recombine with alpha
            return np.dstack([rgb, alpha])
        
        return img_array
    
    def _apply_wand_effects(self, img_array: np.ndarray) -> np.ndarray:
        """Apply ImageMagick effects for professional look"""
        if not WAND_AVAILABLE:
            return img_array
        
        try:
            with WandImage.from_array(img_array) as wand_img:
                # Professional sharpening
                wand_img.unsharp_mask(radius=0.5, sigma=0.5, amount=1.2, threshold=0.05)
                
                # Subtle enhancement
                wand_img.enhance()
                
                # Very subtle vignette
                wand_img.vignette(sigma=5, x=0, y=0)
                
                return np.array(wand_img)
        except Exception as e:
            print(f"Wand effects failed: {e}")
            return img_array
    
    def _add_text_content(self, img: Image.Image, content: Dict, template: Template) -> Image.Image:
        """Add text content with professional typography"""
        draw = ImageDraw.Draw(img)
        
        # Map content to template areas
        content_mapping = {
            "title": content.get("title") or content.get("main_text", ""),
            "description": content.get("description") or content.get("body", ""),
            "content": content.get("main_text", ""),
            "cta": content.get("cta", ""),
            "attribution": content.get("attribution", "- Based Labs"),
            "slide_number": content.get("slide_number", "1/5")
        }
        
        for area_name, area_config in template.text_areas.items():
            if area_name in content_mapping and content_mapping[area_name]:
                text = content_mapping[area_name]
                self._render_text_area(draw, text, area_config)
        
        return img
    
    def _render_text_area(self, draw: ImageDraw.Draw, text: str, area: TextArea):
        """Render text in a specific area with professional typography"""
        # Get optimal font
        font = self._get_optimal_font(text, area)
        
        # Wrap text if needed
        lines = self._wrap_text(text, area.max_width, font)
        
        # Calculate positioning
        y_position = area.y
        line_height = self._get_line_height(font)
        
        # Center vertically if needed
        if area.alignment == "center":
            total_height = len(lines) * line_height
            y_position += (area.max_height - total_height) // 2
        
        # Draw each line
        for line in lines:
            x_position = self._get_x_position(line, area, font)
            
            # Add text shadow for better readability
            shadow_color = "#000000"
            draw.text((x_position + 2, y_position + 2), line, 
                     fill=shadow_color, font=font)
            
            # Draw main text
            draw.text((x_position, y_position), line, 
                     fill=area.color, font=font)
            
            y_position += line_height
    
    def _get_optimal_font(self, text: str, area: TextArea) -> ImageFont.FreeTypeFont:
        """Get optimal font size that fits the area"""
        font_size = area.font_size
        min_size = 12
        
        while font_size >= min_size:
            font = self._load_font(font_size)
            if self._text_fits_area(text, font, area):
                return font
            font_size -= 2
        
        return self._load_font(min_size)
    
    def _load_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Load font with caching"""
        cache_key = f"inter_{size}"
        
        if cache_key not in self.font_cache:
            font_path = self.fonts_dir / "Inter-Bold.ttf"
            
            if font_path.exists():
                self.font_cache[cache_key] = ImageFont.truetype(str(font_path), size)
            else:
                # Fallback to default font
                try:
                    self.font_cache[cache_key] = ImageFont.truetype("arial.ttf", size)
                except:
                    self.font_cache[cache_key] = ImageFont.load_default()
        
        return self.font_cache[cache_key]
    
    def _wrap_text(self, text: str, max_width: int, font: ImageFont.FreeTypeFont) -> List[str]:
        """Intelligent text wrapping"""
        lines = []
        words = text.split()
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            
            if font.getbbox(test_line)[2] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def _text_fits_area(self, text: str, font: ImageFont.FreeTypeFont, area: TextArea) -> bool:
        """Check if text fits in the designated area"""
        lines = self._wrap_text(text, area.max_width, font)
        line_height = self._get_line_height(font)
        total_height = len(lines) * line_height
        
        return total_height <= area.max_height
    
    def _get_line_height(self, font: ImageFont.FreeTypeFont) -> int:
        """Get line height with proper spacing"""
        bbox = font.getbbox("Ay")
        return int((bbox[3] - bbox[1]) * 1.2)
    
    def _get_x_position(self, line: str, area: TextArea, font: ImageFont.FreeTypeFont) -> int:
        """Calculate x position based on alignment"""
        if area.alignment == "center":
            line_width = font.getbbox(line)[2]
            return area.x + (area.max_width - line_width) // 2
        elif area.alignment == "right":
            line_width = font.getbbox(line)[2]
            return area.x + area.max_width - line_width
        else:  # left alignment
            return area.x


class ImageGeneratorService:
    """Service wrapper for the BasedLabsImageGenerator"""
    
    def __init__(self):
        self.generator = BasedLabsImageGenerator(
            templates_dir="templates",
            fonts_dir="fonts"
        )
    
    async def generate_image_for_content(self, content: GeneratedContent) -> Image.Image:
        """Generate image for content with proper async handling"""
        return await self.generator.generate_image_for_content(content)
    
    async def save_image(self, image: Image.Image, output_path: str) -> str:
        """Save generated image to file"""
        image.save(output_path, "PNG", optimize=True)
        return output_path