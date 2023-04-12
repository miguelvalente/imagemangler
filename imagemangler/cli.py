import typer
import io
from PIL import Image
import cv2
import numpy as np

from imagemangler.core.mangler import deteriorate

WINDOW_SIZE = (800, 600)

def main(image_path: str, quality: int = 70):
    """Mangle an image"""
    original_img = Image.open(io.BytesIO(open(image_path, "rb").read()))
    img = Image.open(io.BytesIO(open(image_path, "rb").read()))

    cv2.namedWindow("Original", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Deteriorated", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Original", WINDOW_SIZE[0], WINDOW_SIZE[1])
    cv2.resizeWindow("Deteriorated", WINDOW_SIZE[0], WINDOW_SIZE[1])

    cv2.imshow("Original", cv2.cvtColor(np.asarray(original_img), cv2.COLOR_RGB2BGR))
    cv2.waitKey(1)

    while True:
        if quality == 1:
            break

        img = deteriorate(img, quality=quality)

        cv2.imshow("Deteriorated", cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR))
        cv2.waitKey(1)

        if not typer.confirm("Do you want to continue?"):
            break

        quality = max(1, quality - 2)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    typer.run(main)