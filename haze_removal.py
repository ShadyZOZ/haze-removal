# -*- coding: utf-8 -*-

import os

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
        try:
            image_path = os.path.join('images', image)
        except Exception as e:
            raise ValueError('invalid \'image\' value')
        if os.path.isfile(image_path):
            self.image = cv2.imread(image_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.I = self.image.astype(np.float64)
            self.height, self.width, _ = self.I.shape
        else:
            raise FileNotFoundError('\'{}\' not found'.format(image))

    def get_dark_channel(self, image):
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (self.local_patch_size, self.local_patch_size)
        )
        dark_channel = cv2.erode(image.min(axis=2), kernel).astype(np.uint8)
        return dark_channel

    def get_atmosphere(self, dark_channel):
        flat_image = self.I.reshape(self.height * self.width, 3)
        flat_dark = dark_channel.ravel()
        pixel_count = number_to_integral(
            self.height * self.width * self.percentage)
        search_idx = (-flat_dark).argsort()[:pixel_count]
        return np.max(flat_image.take(search_idx, axis=0), axis=0)

    def get_transmission(self, dark_channel, A):
        transmission = 1 - self.omega * \
            self.get_dark_channel(self.I / A * 255) / 255
        transmission = np.maximum(transmission, self.tmin)
        if self.refine:
            transmission = self.get_refined_transmission(transmission)
        return transmission

    def get_refined_transmission(self, transmission):
        gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        t = (transmission * 255).astype(np.uint8)
        refined_transmission = cv2.ximgproc.guidedFilter(gray, t, 40, 1e-3)
        return refined_transmission / 255

    def get_recover_image(self, A, transmission):
        tiled_t = np.zeros_like(self.I)
        tiled_t[:, :, 0] = tiled_t[:, :, 1] = tiled_t[:, :, 2] = transmission
        return (self.I - A) / tiled_t + A
