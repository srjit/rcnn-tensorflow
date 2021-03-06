import numpy as np
import cv2

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"



class ImageLoader(object):
    def __init__(self, mean_file):
        self.bgr = True 
        self.scale_shape = np.array([640, 640], np.int32)
        self.crop_shape = np.array([640, 640], np.int32)
        self.mean = np.load(mean_file).mean(1).mean(1)

    def load_img(self, img_file):      
        """ Load and preprocess an image. """
        img = cv2.imread(img_file)

        if self.bgr:
            temp = img.swapaxes(0, 2)
            temp = temp[::-1]
            img = temp.swapaxes(0, 2)

        img = cv2.resize(img, (self.scale_shape[0], self.scale_shape[1]))
        offset = (self.scale_shape - self.crop_shape) / 2
        offset = offset.astype(np.int32)
        img = img[offset[0]:offset[0]+self.crop_shape[0], offset[1]:offset[1]+self.crop_shape[1], :]
        img = img - self.mean
        return img

    def load_imgs(self, img_files):
        """ Load and preprocess a list of images. """
        imgs = []
        for img_file in img_files:
            imgs.append(self.load_img(img_file))
        imgs = np.array(imgs, np.float32)
        return imgs
