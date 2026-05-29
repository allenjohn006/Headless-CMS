from PIL import Image
import os
from io import BytesIO

def optimize_image(file_data: bytes, output_path: str, max_width: int = 1200):
    """
    Optimizes and converts an image to WebP format, resizing it if it exceeds max_width.
    """
    try:
        with Image.open(BytesIO(file_data)) as img:
            # Convert to RGB if necessary (e.g. RGBA -> RGB for some formats, though WEBP supports RGBA)
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA")
                
            # Resize if too large
            if img.width > max_width:
                ratio = max_width / img.width
                new_size = (max_width, int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                
            # Save as WebP
            img.save(output_path, "WEBP", quality=80)
            return True
    except Exception as e:
        print(f"Error optimizing image: {e}")
        return False
