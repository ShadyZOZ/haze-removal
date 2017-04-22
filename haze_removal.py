# -*- coding: utf-8 -*-

import os

from PIL import Image
import cv2
import numpy as np

from utils import number_to_integral


class HazeRemovel():

    def __init__(self, image='ny1.bmp', refine=True, local_patch_size=15,
                 omega=0.95, percentage=0.001, tmin=0.2):
        self.refine = refine
        self.local_patch_size = local_patch_size
        self.omega = omega
        self.percentage = percentage
        self.tmin = tmin
        self.image_name = image
        if os.path.isfile(image):
            image = Image.open(image)
            self.image = np.asarray(image, dtype=np.uint8)
            # image = cv2.imread(image)
            # self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.I = self.image.astype(np.float64)
            self.height, self.width, _ = self.I.shape
        else:
            raise FileNotFoundError('\'{}\' not found'.format(image))

    def get_dark_channel(self, image):
        min_image = image.min(axis=2)
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (self.local_patch_size, self.local_patch_size)
        )
        dark_channel = cv2.erode(min_image, kernel).astype(np.uint8)
        return dark_channel

    def get_atmosphere(self, dark_channel):
        img_size = self.height * self.width
        flat_image = self.I.reshape(img_size, 3)
        flat_dark = dark_channel.reshape(img_size, 1)
        pixel_count = number_to_integral(img_size * self.percentage)
        search_idx = (-flat_dark).argsort()[:pixel_count]
        atm_sum = np.zeros([1, 3])
        for i in range(pixel_count):
            atm_sum = atm_sum + flat_image[search_idx[i]]
        return atm_sum / pixel_count

    def get_transmission(self, dark_channel, A):
        transmission = 1 - self.omega * \
            self.get_dark_channel(self.I / A * 255.0) / 255.0
        transmission = np.maximum(transmission, self.tmin)
        if self.refine:
            transmission = self.get_refined_transmission(transmission)
        return transmission

    def get_refined_transmission(self, transmission):
        # gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        gray = self.image.min(axis=2)
        t = (transmission * 255).astype(np.uint8)
        refined_transmission = cv2.ximgproc.guidedFilter(gray, t, 40, 1e-2)
        return refined_transmission / 255

    def get_recover_image(self, A, transmission):
        tiled_t = np.zeros_like(self.I)
        tiled_t[:, :, 0] = tiled_t[:, :, 1] = tiled_t[:, :, 2] = transmission
        return (self.I - A) / tiled_t + A
