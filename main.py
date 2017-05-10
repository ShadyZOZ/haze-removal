# -*- coding: utf-8 -*-

import fire
from PIL import Image

from haze_removal import HazeRemovel
from utils import threshold_color_array


class Cli():

    def __init__(self, image='ny1.bmp', refine=True, w=15,  omega=0.95,
                 p=0.001, tmin=0.1, mean=False, save=False):
        if not isinstance(refine, bool):
            raise ValueError('invalid \'refine\' value')
        self.haze_removal = HazeRemovel(
            image=image,
            refine=refine,
            local_patch_size=w,
            omega=omega,
            percentage=p,
            tmin=tmin,
            mean=mean,
        )
        self.save = save

    def show_image(self):
        self._show_image(self.haze_removal.image, title='org')

    def show_dark_channel(self):
        dark_channel = self.haze_removal.get_dark_channel(self.haze_removal.I)
        self._show_dark_channel(dark_channel)

    def _show_dark_channel(self, dark_channel):
        self._show_image(dark_channel, title='dark')

    def show_transmission(self):
        dark_channel = self.haze_removal.get_dark_channel(self.haze_removal.I)
        A = self.haze_removal.get_atmosphere(dark_channel)
        t = self.haze_removal.get_transmission(dark_channel, A)
        self._show_transmission(t)

    def _show_transmission(self, t):
        self._show_image(t * 255, title='t', threshold=True)

    def show_recover_image(self):
        dark_channel = self.haze_removal.get_dark_channel(self.haze_removal.I)
        A = self.haze_removal.get_atmosphere(dark_channel)
        t = self.haze_removal.get_transmission(dark_channel, A)
        recover_image = self.haze_removal.get_recover_image(A, t)
        self._show_recover_image(recover_image)

    def _show_recover_image(self, recover_image):
        self._show_image(recover_image, title='res', threshold=True)

    def recover(self):
        dark_channel = self.haze_removal.get_dark_channel(self.haze_removal.I)
        A = self.haze_removal.get_atmosphere(dark_channel)
        print('atmosphere value: {}'.format(A))
        t = self.haze_removal.get_transmission(dark_channel, A)
        recover_image = self.haze_removal.get_recover_image(A, t)
        self.show_image()
        self._show_dark_channel(dark_channel)
        self._show_transmission(t)
        self._show_recover_image(recover_image)

    def _show_image(self, image, title='', threshold=False):
        if threshold:
            image = threshold_color_array(image)
        image = Image.fromarray(image)
        if self.save:
            if title != 'dark':
                name, ext = self.haze_removal.image_name.split('.')
                image.save('results/{0}_{1}.jpg'.format(name, title))
        else:
            image.show()


def main():
    try:
        fire.Fire(Cli)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
