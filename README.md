# image-plagiarizing-detector


Photographers upload their photos online, and often other people would crop a portion the photos and use the cropped versions without permission.  This application helps solves the problem of photographers' need for content protection.

## Getting Started

### Prerequisites & Packages

* Python
* numpy
* Pillow
* scikit-image


### Installing

Clone the repository and unzip the contents. Open your computer terminal and change directory to be located inside the repository.

## GUI Preview  


[alt text](https://raw.githubusercontent.com/glennsvel90/image-plagiarizing-detector/master/GuiPreview.PNG "GUI Preview")


## Methodology

The main function that does the bulk of the work is the Match Template Function. It takes a smaller image and finds where it closely resembles a larger original image. The limitations of just using this function is that the runtime for large images tends to be large. Runtime can become 10 times faster, if
a multi-step process is taken when using the Match Template Function. The steps are as follows:

1. Check to see if the suspect image is smaller than the original image
2. Compare both images to a size threshold to prevent excessive runtime length during processing
3. Convert the image to gray scale to further reduce runtime by one-third
4. Find a location in the larger original image where there is most resemblance to the suspect image
5. Cut the larger image the same size as the suspect image, with the cutting occurring around the area of most resemblance. The new cut up image is called the subset
6. Apply an image channel subtraction operation between the new subset and the suspect image. If the difference from the subtraction has a lower RMS value than a threshold, the image has been plagiarized.
