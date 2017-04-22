# -*- coding: utf-8 -*-

import cv2
import numpy as np


def number_to_integral(number):
    return int(np.ceil(number))


def threshold_color_array(src):
    # retval, dst = cv2.threshold(src, 255, 255, cv2.THRESH_TRUNC)
    # retval, dst = cv2.threshold(
    #     dst,
    #     0, 255, cv2.THRESH_TOZERO
    # )
    # return dst.astype(np.uint8)
    return np.maximum(np.minimum(src, 255), 0).astype(np.uint8)
