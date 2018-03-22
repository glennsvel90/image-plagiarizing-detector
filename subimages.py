import os
import numpy as np
from math import sqrt
from time import time
from queue import queue
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageChops
from skimage.feature import match_template

MAX_WIDTH = 650
MAX_HEIGHT = 650
RMS_THRESHOLD = 50

class FindPlagiarized:

    def __init__(self, master):
        self.master = master
        self.master.title('Find Plagiarized Images')
        self.master.resizable(False, False)

        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(padx = 5, pady = 5) # put padding when packing

        ttk.Label(self.main_frame, text = 'Search Directory:').grid(row = 0, column = 0, sticky = 'w')
        self.path_entry = ttk.Entry(self.main_frame, width = 54)
        self.path_entry.grid(row = 1, column = 0, sticky = 'e')
        self.path_entry.insert(0, '.\\images') # make default search folder
        self.browse_button = ttk.Button(self.main_frame, text = 'Browse...',
                                        command = self.browse_callback)
        self.browse_button.grid(row = 1, column =1, sticky = 'w')

        self.search_button = ttk.Button(self.main_frame, text = 'Find Plagiarized Images',
                                        command = self.search_callback)
        self.search_button.grid(row = 2, column = 0, columnspan = 2)

        self.results_table = ttk.Treeview(self.main_frame, column = ('subset'))
        self.results_table.heading('#0', text = 'Original Image')
        self.results_table.column('#0', width = 200)
        self.results_table.heading('subset', text = 'Subset Image')
        self.results_table.column('subset', width = 200)

    def browse_callback(self):
        path = filedialog.askdirectory(initialdir = self.path_entry.get())
        self.path_entry.delete(0, END)
        self.path_entry.insert(0, path)

    def search callback(self):

    def process_queue(self):
        # get a pair of images to analyze. These pairs are tuples.
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

                # resize images based on ratio
                orig_img = orig_img.resize((int(ratio*orig_img.size[0]),
                                                int(ratio*orig_image.size[1])),
                                                Image.ANTIALIAS)
                temp_img = temp_img.resize((int(ratio*temp_img.size[0]),
                                            int(ratio*temp_img.size[1])),
                                            Image.ANTIALIAS)
            else:
                ratio = 1

            #turn the images to grayscale arrays using numpy module
            orig_arr = np.array(orig_img.convert(mode = 'L'))
            temp_arr = np.array(temp_img.convert(mode = 'L'))

            # come up with a correlation match array of the original array that most resembles the template array
            match_arr = match_template(orig_arr, temp_arr)
            # find the exact location coordinates of the area of the match array that most resembles the template array
            match_loc = np.unravel_index(np.argmax(match_arr), match_arr.shape)

            # if the images were resized, go back to the full-sized original color image(not the template image) and resize it back to the original dimensions and re-import them
            # to later use the exact locations coordinates obtained above to crop the image to the size of the template suspect image
            if ratio != 1:
                match_loc = (int(match_loc[0]/ratio), int(match_loc[1]/ratio))
                #re-import the images
                orig_img =Image.open(os.path.join(self.path, pair[0]))
                temp_img = Image.open(os.path.join(self.path, pair[1]))

            # convert the original image to a numpy array, then index out the length ranges to keep in both x and y axis of the original image, keeping the match_loc coordinates in the
            # top left corner of where the oringal image starts to resemble the template image. When indexing occurs, the x range to crop the original photo will be from the start of the
            # match loc coordinate's x-value to the entire x-value range of the template image size. The y range to crop the original photo will be from the start of the of the
            # math loc coordinate's y-value to the entire y-value range of the template image size. This will get the matching subsection from the original image
            orig_sub_arr = np.array(orig_img)[match_loc[0]:match_loc[0] + temp_img.size[0],
                                                match_loc[1]:match_loc[1] + temp_img.size[1]]
            # turn image to color, this is what we finally believe to be the match to the suspect image. But we have to test compare this image with the
            #temp image using the imagechops module and seeing if the rms value after the test is smaller than the RMS threshold of 50
            orig_sub_img = Image.fromarray(orig_sub_arr, mode = 'RGB')


            #find the difference between the cropped subsection image and the template suspect image, we calculate the pixel by pixel image difference between
            #the two images using image channel operations(ImageChOp) module. If images are identical, the output is nearly zero. Then call the histogram function
            # on the output h_diff. h_diff is a list of 768 values that each tell the number of pixels for certain red, green, and blue colors. The first 256 values are
            #for certain red colors. The second 256 values are for certain blue colors, and the last set of 256 values of h_diff are for certain green colors.
            h_diff = ImageChops.difference(orig_sub_img, temp_img).histogram()

            # find the sum of squares for every set in the enumerate(h_diff). To do this, the color value is represented by the "index(idx) modulo 256."
            #This would always result in a number between 0 and 255. Square the color value, and multiply that by the number of pixels in the image that
            # have that color value in that iteration. The number of pixels is the that iteration's h_diff value.
            sum_of_squares = sum(value * ((idx % 256) **2) for idx, value in enumerate(h_diff))

            #find the area (total number of pixels) of the template suspect image, indexed by x and y values
            temp_img_area = float(temp_img.size[0]*temp_img.size[1])

            # find the RMS(root mean square) value
            rms = sqrt(sum_of_squares/temp_img_area)

            if RMS_THRESHOLD > rms: # add matches to table
                self.results_table.grid(row = 3, column = 0, columnspan = 2, padx = 5, pady =5)
                self.results_table.insert('', 'end', str(self.progress_var.get()), text = pair[0])
                self.results_table.set(str(self.progress_var.get()), 'subset', pair[1])
                self.results_table.config(height = len(self.results_table.get_children('')))

        self.progressbar.step()
        self.status_var.set('Analyzed {} vs {} - {} pairs remaining...'.format(pair[0], pair[1], self.queue.qsize()))

        if not self.queue.





            # divide the sum of squares by the number of pixels in the image and takes the square root of that to get the RMS value












def main():
    root = Tk()
    FindSubset(root)
    root.mainloop()
