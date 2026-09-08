import base64
import os
import aiofiles

async def convert_file_to_base64(file_path: str) -> tuple[str, int]:
    async with aiofiles.open(file_path, "rb") as f:
        data = await f.read()
    
    encoded_bytes = base64.b64encode(data)
    encoded_str = encoded_bytes.decode("utf-8")
    return encoded_str, len(encoded_bytes)

def generate_data_uri(base64_str: str, mime_type: str) -> str:
    return f"data:{mime_type};base64,{base64_str}"

async def save_base64_to_temp_file(content: str, prefix: str) -> str:
    os.makedirs("temp_downloads", exist_ok=True)
    temp_path = os.path.join("temp_downloads", f"{prefix}.txt")
    async with aiofiles.open(temp_path, "w", encoding="utf-8") as f:
        await f.write(content)
    return temp_path
