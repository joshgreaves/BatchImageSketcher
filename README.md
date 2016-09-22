# Batch Image Sketcher
### About
Batch image sketcher is a programme written in python designed to explore every file in a directory, and if it is an image file create a "sketched" version of it.

### Example
Before:
![Image before](https://github.com/joshgreaves/BatchImageSketcher/blob/master/images/Before3.jpg)
After:
![Image after](https://github.com/joshgreaves/BatchImageSketcher/blob/master/images/after3.jpg)

### Prerequesites
Python, OpenCV, numpy.
To install OpenCV: `sudo apt-get install python-opencv`
To install numpy: `sudo pip install numpy`

### Usage
1. cd to the directory you want to clone to
2. `git clone https://github.com/joshgreaves/BatchImageSketcher`
3. `cd BatchImageSketcher`
4. `python main.py path_to_folder_to_get_images_from path_to_folder_to_save_images_to` (The two directories must already exist)
5. The images will be "sketched" and saved in the directory you specified, in the same place with the same name.
