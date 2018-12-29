from urllib import request
import cv2
import numpy as np


def get_image_from_url(url):
    resp = request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image
    