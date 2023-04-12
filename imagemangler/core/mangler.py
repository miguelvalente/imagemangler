from PIL import Image
import io

def deteriorate(image_path: str, iterations: int = 1, optimize: bool = False, quality: int = 20) -> None:
    """Deteriorate the image by 50% quality for `iterations` number of times"""

    # Open the original image file
    with open(image_path, 'rb') as f:
        # Load the image from the file
        img = Image.open(io.BytesIO(f.read()))

    for i in range(iterations):
        # Compress the image
        compressed_buffer = io.BytesIO()
        img.save(compressed_buffer, format='JPEG', optimize=optimize, quality=quality)

        # Get the compressed image data as bytes
        compressed_bytes = compressed_buffer.getvalue()

        # Load the compressed image into a PIL.Image object
        img = Image.open(io.BytesIO(compressed_bytes))

    # Load the original image into a PIL.Image object
    original_img = Image.open(io.BytesIO(open(image_path, 'rb').read()))

    # Show the original and final deteriorated images
    original_img.show()
    img.show()

if __name__ == '__main__':
    deteriorate("imagemangler/book.webp", 5)
