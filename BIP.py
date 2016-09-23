import cv2
import os
import Queue
import time

import numpy as np

from threading import Thread
from tqdm import tqdm


class BatchImageProcessor():
    def __init__(self, number_of_threads = 12):
        # Constants
        self.NUM_THREADS = number_of_threads

        #Useful variables
        self.image_count = 0

    def batch_sketchify(self, source_path, dest_path):
        print "About to start sketching the batch"

        # Cache the paths
        self.SOURCE = source_path
        self.DEST = dest_path

        # We will need a queue
        self.q = Queue.Queue()
        self.working = True

        # We will do this with 12 threads
        self.threads = []
        for i in range(self.NUM_THREADS):
            thread = Thread(target=self.sketch_worker)
            self.threads.append(thread)
        
        # Start all the threads
        for t in self.threads:
            t.start()
        
        # Gets the paths, subfolders, and files in the whole source
        for path, subFolders, files in tqdm(os.walk(self.SOURCE)):
            self.q.put((path, files))

        # Print how many directories are left to process
        while (self.q.qsize() > 0):
            print str(self.q.qsize()) + " directories left to proces..."
            time.sleep(1)

        print "left the loop..."
        
        # Let the threads know we're done
        self.working = False
        
        # Wait for all the threads to finish
        for t in self.threads:
            print "joining threads..."
            t.join()
        
        # Finish!
        print "All sketched!"
    

    def sketch_worker(self):
        # While the main thread is still looking for images
        while self.working:
            # Ensure there is something on the queue
            if not self.q.empty():
                # Need to try in case there is nothing in the list
                try:
                    dir, files = self.q.get(True, 1) #Will block the thread for 1 second before throwing an empty exception
                except Queue.Empty:
                    break

                self.sketchify_all_in_directory(dir, files)
                self.q.task_done()
            else:
                # If there is nothing on the queue, just wait a fraction of a second
                time.sleep(0.1)
        
        return


    def sketchify_all_in_directory(self, dir, files):
        # Get the current relative path
        rel_path = os.path.relpath(dir, self.SOURCE)

        # Make sure the path exists in the destination
        if not os.path.exists(os.path.join(self.DEST, rel_path)):
            os.mkdir(os.path.join(self.DEST, rel_path))

        # Gets every picture in the directory
        for pic in (pic for pic in files if pic.lower().endswith(('.png', '.jpg', '.jpeg'))):
    
            # Get the image name without extension
            pre, ext = os.path.splitext(pic)
    
            # If the image already exists, don't sketch it!
            if (not os.path.isfile(os.path.join(self.DEST, rel_path, pre + ".png"))):
    
                # Count another image processed
                self.image_count += 1
    
                # Print status after every 1000 images
                if self.image_count % 1000 == 0:
                    print "Image Count: " + str(self.image_count)
    
                # Actually sketch the image    
                img = self.sketchify(os.path.join(dir, pic))
    
                # Change the extension and write file
                cv2.imwrite(os.path.join(self.DEST, rel_path, pre + ".png"), img)

                #print "SAVING IMAGE! " + os.path.join(DESTINATION_PATH, rel_path, pre + ".png")
                #print os.path.join(path, pic)


    # Will sketchify a single image
    def sketchify(self, img_path):
        img = cv2.imread(img_path, 0)
        inv = 255 - img
        b_inv = cv2.GaussianBlur(inv, (15, 15), 0)
        return cv2.divide(img, 255-b_inv, scale=256)
