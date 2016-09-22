import cv2
import time
import numpy as np
import argparse
import os
from tqdm import tqdm
import Queue
from threading import Thread

image_count = 0
MAX_THREADS = 12
q = Queue.Queue()
DESTINATION_PATH = ""
SOURCE_PATH = ""

# Will sketchify a single image
def sketchify(img_path):
    img = cv2.imread(img_path, 0)
    inv = 255 - img
    b_inv = cv2.GaussianBlur(inv, (15, 15), 0)
    return cv2.divide(img, 255-b_inv, scale=256)


# Will sketchify every image in a directory, and traverse every directory from the current one down
def recursive_sketchify(source_path, dest_path):

    print "Entering directory: " + source_path

    # Get a list of all pictures and directories in the current directory
    list_of_files_and_directories = os.listdir(source_path)

    # Base case: There are no more files or directories
    if len(list_of_files_and_directories) == 0:
        return

    # To make things easier, ensure both paths end with /
    if not source_path.endswith('/'):
        source_path += '/'
    if not dest_path.endswith('/'):
        dest_path += '/'
    
    #Collect the directories together and the files together
    directories = []
    picture_files = []

    # Seperate into a list of files and list of directories
    for f in list_of_files_and_directories:
        if (os.path.isdir(source_path + f)):
            directories.append(f)
            # Also create the directory in the destination
            if not os.path.exists(dest_path + f):
                #print "Making directory: " + dest_path + f
                os.makedirs(dest_path + f)
        elif (os.path.isfile(source_path + f) and f.lower().endswith(('.png', '.jpg', '.jpeg'))):
            picture_files.append(f)
        else:
            print "\t" + f + " wasn't a directory or picture file"
    
    #print "Directories", directories
    #print "Picture files", picture_files

    # While there is a directory in the list:
    while (len(directories) > 0):
        # Enter a directory, appending its name to the destination path
        recursive_sketchify(source_path + directories[0] + '/', dest_path + directories[0] + '/')

        # When it has returned we can delete the directory from the list
        del directories[0]
    
    # Since there are no more directories here, let's grab the pictures!
    while (len(picture_files) > 0):

        # Get the image name without extension
        pre, ext = os.path.splitext(picture_files[0])

        # If the image already exists, don't sketch it!
        if (not os.path.isfile(dest_path + pre + ".png")):

            # Count another image processed
            global image_count
            image_count += 1

            # Print status after every 1000 images
            if image_count % 1000 == 0:
                print "Image Count: " + str(image_count)
            img = sketchify(source_path + picture_files[0])

            # Change the extension and write file
            cv2.imwrite(dest_path + pre + ".png", img)
            print "SAVING IMAGE! " + dest_path + picture_files[0]

        del picture_files[0]
    
    return

def sketchify_all_in_directory(path, files):
    global DESTINATION_PATH
    global SOURCE_PATH

    # Gets every picture in the domain
    for pic in (pic for pic in files if pic.lower().endswith(('.png', '.jpg', '.jpeg'))):

        # Get the current relative path
        rel_path = os.path.relpath(path, SOURCE_PATH)
        #print "rel path: " + rel_path

        # Get the image name without extension
        pre, ext = os.path.splitext(pic)

        # If the image already exists, don't sketch it!
        if (not os.path.isfile(os.path.join(DESTINATION_PATH, rel_path, pre + ".png"))):

            # Count another image processed
            global image_count
            image_count += 1

            # Print status after every 1000 images
            if image_count % 1000 == 0:
                print "Image Count: " + str(image_count)

            # Actually sketch the image    
            img = sketchify(path + pic)

            # Change the extension and write file
            cv2.imwrite(os.path.join(DESTINATION_PATH, rel_path, pre + ".png"), img)
            #print "SAVING IMAGE! " + os.path.join(DESTINATION_PATH, rel_path, pre + ".png")
		    #print os.path.join(path, pic)

def runner():
    global q
    time.sleep(3)
    while not q.empty():
        dir, files = q.get()
        sketchify_all_in_directory(dir, files)
    
    return



def smarter_sketchify(source_path, dest_path):
    global q

    print "Finding all images..."

    threads = []
    # Start a thread for each 
    for i in range(MAX_THREADS):
        print "Starting thread " + str(i)
        thread = Thread(target=runner)
        threads.append(thread)
    
    for x in threads:
        x.start()
    
    # Gets the paths, subfolders, and files in the whole source
    for path, subFolders, files in tqdm(os.walk(source_path)):
        q.put((path, files))
    
    while q.qsize() > 0:
        print q.qsize() + " directories left to proces..."
        time.sleep(1)

    for x in threads:
        x.join()
        
    

    sketchify_all_in_directory(path, files)
        


#cv2.imshow(str(i), dodged)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#img = cv2.imread('/home/josh/Desktop/test' + str(i) + '.JPEG', 0)

# Prepare argparse
parser = argparse.ArgumentParser(description="Sketchify all images recursively from a directory.")
parser.add_argument('path', type=str, nargs=2, help="The directory to get the images from, and the directory to save it to")
args = parser.parse_args()

# Check that two arguments were passed in
if len(args.path) != 2:
    print "You must pass in exactly two paths"
    exit()

# The first argument is the path to get the images from
SOURCE_PATH = args.path[0]
# The second argument is the path to save the images to
DESTINATION_PATH = args.path[1]

# Check that the paths exist
if not os.path.isdir(SOURCE_PATH):
    print SOURCE_PATH + " doesn't exist."
    print "Exiting..."
    exit()
if not os.path.isdir(DESTINATION_PATH):
    print DESTINATION_PATH + " doesn't exist."
    print "Exiting..."
    exit()

#recursive_sketchify(SOURCE_PATH, DESTINATION_PATH)
smarter_sketchify(SOURCE_PATH, DESTINATION_PATH)