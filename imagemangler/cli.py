import concurrent.futures
import io
import threading
import zipfile

import cv2
import numpy as np
import typer
from PIL import Image

from imagemangler.core.mangler import deteriorate


app = typer.Typer()


WINDOW_SIZE = (800, 600)


def zip_image(zip_file, img, name, extension):
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=extension)
    zip_file.writestr(f"{name}.{extension}", img_bytes.getvalue())


@app.command()
def main(
    image_path: str,
    quality: int = typer.Argument(70, help="Base quality to start with"),
    quality_step: int = typer.Option(2, help="Quality step to reduce by"),
    auto_mangle: bool = typer.Option(
        False, help="Automatically mangle the image across all qualitie steps"
    ),
):
    """
    Mangle an image by deteriorating it iteratively with
    quality reduction of lossy algorithms
    """

    original_img = Image.open(io.BytesIO(open(image_path, "rb").read()))
    img = Image.open(io.BytesIO(open(image_path, "rb").read()))

    cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Deteriorated", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Original", WINDOW_SIZE[0], WINDOW_SIZE[1])
    cv2.resizeWindow("Deteriorated", WINDOW_SIZE[0], WINDOW_SIZE[1])

    cv2.imshow("Original", cv2.cvtColor(np.asarray(original_img), cv2.COLOR_RGB2BGR))
    cv2.waitKey(1)

    mangled_images = []
    while True:
        img = deteriorate(img, quality=quality)
        mangled_images.append(img)

        cv2.imshow("Deteriorated", cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR))
        cv2.waitKey(2)

        if not auto_mangle:
            if not typer.confirm("Mangle again?", default=True):
                break

        quality = max(0, quality - quality_step)
        if quality == 0:
            break

    if auto_mangle:
        cv2.waitKey(0)
    cv2.destroyAllWindows()

    extension = image_path.split(".")[-1]
    if typer.confirm("Do you want to save all mangled images?"):
        with zipfile.ZipFile("mangled_images.zip", "w") as zip_file:
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
