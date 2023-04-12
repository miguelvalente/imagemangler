import io

import cv2
import numpy as np

WINDOW_SIZE = (1100, 900)


def zip_image(zip_file, img, name, extension):
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=extension)
    zip_file.writestr(f"{name}.{extension}", img_bytes.getvalue())


def show_image(img):
    cv2.namedWindow("Deteriorated", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Deteriorated", WINDOW_SIZE[0], WINDOW_SIZE[1])
    cv2.imshow("Deteriorated", cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR))
    cv2.waitKey(1)
