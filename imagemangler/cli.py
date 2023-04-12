import concurrent.futures
import io
import zipfile

import cv2
import typer
from PIL import Image

from imagemangler.core.mangler import deteriorate
from imagemangler.core.utils import show_image, zip_image

app = typer.Typer()


@app.command()
def main(
    image_path: str,
    quality: int = typer.Argument(70, help="Base quality to start with"),
    quality_step: int = typer.Option(2, help="Quality step to reduce by"),
    auto_mangle: bool = typer.Option(
        True, help="Automatically mangle the image across all quality steps"
    ),
):
    """
    Mangle an image by deteriorating it iteratively with
    quality reduction of lossy algorithms
    """
    img = Image.open(io.BytesIO(open(image_path, "rb").read()))

    mangled_images = []
    while True:
        img = deteriorate(img, quality=quality)
        mangled_images.append(img)

        show_image(img)

        if not auto_mangle:
            if not typer.confirm("Mangle again?", default=True):
                break

        quality = max(0, quality - quality_step)
        if quality == 0:
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    extension = image_path.split(".")[-1]
    if typer.confirm("Do you want to save all mangled images?"):
        with zipfile.ZipFile("mangled_images.zip", "w") as zip_file:
            # for faster zipping, use concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for i, img in enumerate(mangled_images):
                    futures.append(
                        executor.submit(
                            zip_image, zip_file, img, f"mangled_img_{i}", extension
                        )
                    )
                concurrent.futures.wait(futures)

    elif typer.confirm("Do you want to save the last mangled image?"):
        img.save(f"mangled_img.{extension}")

if __name__ == "__main__":
    app()