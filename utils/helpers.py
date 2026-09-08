import os
from PIL import Image

def format_size(size_in_bytes: int) -> str:
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.2f} KB"
    else:
        return f"{size_in_bytes / (1024 * 1024):.2f} MB"

def get_image_metadata(file_path: str) -> dict:
    with Image.open(file_path) as img:
        width, height = img.size
        img_format = img.format.upper() if img.format else "UNKNOWN"
    
    file_size = os.path.getsize(file_path)
    
    mime_type_map = {
        "JPEG": "image/jpeg",
        "PNG": "image/png",
        "WEBP": "image/webp",
        "GIF": "image/gif"
    }
    mime_type = mime_type_map.get(img_format, f"image/{img_format.lower()}")

    return {
        "filename": os.path.basename(file_path),
        "format": img_format,
        "mime_type": mime_type,
        "width": width,
        "height": height,
        "size_bytes": file_size,
        "size_formatted": format_size(file_size)
    }

def safe_remove_file(file_path: str) -> None:
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except OSError:
            pass
