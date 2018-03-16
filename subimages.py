import os
import numpy as np
from math import sqrt
from time import time
from queue import queue
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageChops
from skimage.feature import match_template

MAX_WIDTH = 640
MAX_HEIGHT = 640
RMS_THRESHOLD = 50

class FindSubset:

    def __init__(self, master):

    def browse_callback(self):

    def search callback(self):

    def process_queue(self):
        # get a pair of images to analyze
        pair = self.queue.get()
        orig_img = Image.open(os.path.join(self.path, pair[0]))
        temp_img = Image.open(os.path.join(self.path, pair[1]))

        # check that the original image is larger than the template image in the x and y axis, if check fails, pick other pair of images to be analyzed from
        # the queue
        if (temp_img.size[0] < orig_img.size[0]) and (temp_img.size[1] < orig_img.size[1]):

            # find out if images need to be resized smaller
            if (orig_img[0] > MAX_WIDTH) or (orig_img.size[1] > orig_img.size[1] > MAX_HEIGHT):
                # calculate ratio for resizing
                ratio = min(MAX_WIDTH/float(orig_img.size[0]),
                            MAX_HEIGHT/float(orig_img.size[1]))

                




def main():
    root = Tk()
    FindSubset(root)
    root.mainloop()
