import cv2
import math
import numpy as np


def draw_text(image, text, center, angle, 
    font=cv2.FONT_HERSHEY_SIMPLEX,
    fontScale=1, 
    color=(255,255,255),
    thickness=4):

    # draw text_layer
    text_layer = np.zeros_like(image)
    anchor = get_text_anchor(text, center)
    cv2.putText(text_layer, text, tuple(anchor), font, fontScale, color, thickness)
    text_layer = rotate_image(text_layer, angle, tuple(center))
    image = overlay(text_layer, image)
    return image


def get_text_anchor(text, center):
    font = cv2.FONT_HERSHEY_SIMPLEX
    # get boundary of this text
    text_size = cv2.getTextSize(text, font, 1, 4)[0]
    offset = np.asarray(text_size) * [-0.5, 0.5]
    anchor = center + offset
    return anchor.astype(np.int)


def rotate_image(image, angle, anchor):
    """Rotate image by angle around anchor point. 
    Args:
        image: image as opened by cv2
        angle: in radians, counter-clockwise
        anchor: rotation point of origin, in form [x, y]
    Returns 
        rotated image. 
    """
    row, col, _ = image.shape
    degrees = angle * 180 / math.pi
    rot_mat = cv2.getRotationMatrix2D(anchor,degrees,1.0)
    new_image = cv2.warpAffine(image, rot_mat, (col, row))
    return new_image


def overlay(text, image):
    """Overlay text on top of image. 
    NOTE: assumes white / light color text on black background. 
    """
    # Now create a mask of text and create its inverse mask also
    img2gray = cv2.cvtColor(text,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 127.5, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # Now black-out the area of logo in ROI
    img1_bg = cv2.bitwise_and(image, image, mask=mask_inv)
    # Take only region of logo from logo image.
    img2_fg = cv2.bitwise_and(text, text, mask=mask)
    # Put logo in ROI and modify the main image
    dst = cv2.add(img1_bg,img2_fg)
    return dst