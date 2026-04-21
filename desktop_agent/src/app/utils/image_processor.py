"""Image Processing for Screenshots"""
from PIL import Image
import io
from typing import Tuple


class ImageProcessor:
    """Process screenshots before upload"""
    
    def __init__(self, max_width: int = 1920, quality: int = 70):
        self.max_width = max_width
        self.quality = quality
    
    def process(self, image: Image.Image) -> bytes:
        """
        Convert screenshot to optimized JPEG
        - Convert to RGB if RGBA
        - Resize if width > max_width (maintain aspect ratio)
        - Compress to JPEG with specified quality
        """
        # Convert to RGB if needed
        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if too large
        if image.width > self.max_width:
            ratio = self.max_width / image.width
            new_height = int(image.height * ratio)
            image = image.resize((self.max_width, new_height), Image.LANCZOS)
        
        # Save as JPEG
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=self.quality, optimize=True)
        return output.getvalue()
    
    def get_image_info(self, image: Image.Image) -> dict:
        """Get image information"""
        return {
            'width': image.width,
            'height': image.height,
            'mode': image.mode,
            'format': 'JPEG'
        }
