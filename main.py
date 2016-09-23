import argparse
import os

from BIP import BatchImageProcessor

# Prepare argparse
parser = argparse.ArgumentParser(description="Sketchify all images recursively from a directory.")
parser.add_argument('SOURCE_PATH', type=str, nargs=1, help="The directory to get the images from")
parser.add_argument('DEST_PATH', type=str, nargs=1, help="The directory to save the images to")
args = parser.parse_args()

# Check that two arguments were passed in
if not args.SOURCE_PATH or not args.DEST_PATH:
    print "You must pass in exactly two paths. Exiting."
    exit()

SOURCE_PATH = args.SOURCE_PATH[0]
DEST_PATH = args.DEST_PATH[0]

# Check that the paths exist
if not os.path.isdir(SOURCE_PATH):
    print SOURCE_PATH + " doesn't exist."
    print "Exiting..."
    exit()
if not os.path.isdir(DEST_PATH):
    print DEST_PATH + " doesn't exist."
    print "Exiting..."
    exit()

# Get a batch image processor
b = BatchImageProcessor()

# Batch sketch everything
b.batch_sketchify(SOURCE_PATH, DEST_PATH)