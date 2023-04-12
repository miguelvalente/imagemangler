import io

import cv2
import numpy as np

WINDOW_SIZE = (1100, 900)


def zip_images(zip_file, images, extension):
    for i, img in enumerate(images):
        with io.BytesIO() as f:
            img.save(f, format=extension)
            f.seek(0)
            zip_file.writestr(f"mangled_img_{i}.{extension}", f.read())


def show_image(img):
    cv2.namedWindow("Deteriorated", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Deteriorated", WINDOW_SIZE[0], WINDOW_SIZE[1])
    cv2.imshow("Deteriorated", cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR))
    cv2.waitKey(1)
