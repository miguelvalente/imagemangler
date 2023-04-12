from PIL import Image
import io


def deteriorate(
    img: Image, optimize: bool = True, quality: int = 20
) -> Image:
    """Deteriorate the image quality for `iterations` number of times"""

    compressed_buffer = io.BytesIO()
    img.save(compressed_buffer, format="JPEG", optimize=optimize, quality=quality)

    # Get the compressed image data as bytes
    compressed_bytes = compressed_buffer.getvalue()

    # Load the compressed image into a PIL.Image object
    img = Image.open(io.BytesIO(compressed_bytes))

    return img