import io

from PIL import Image


def deteriorate(
    img: Image,
    extension,
    optimize: bool = True,
    quality: int = 20,
) -> Image:
    """Deteriorate the image quality for `iterations` number of times"""

    compressed_buffer = io.BytesIO()
    img.save(compressed_buffer, format=extension, optimize=optimize, quality=quality)

    # Get the compressed image data as bytes
    compressed_bytes = compressed_buffer.getvalue()

    # Load the compressed image into a PIL.Image object
    img = Image.open(io.BytesIO(compressed_bytes))

    return img
