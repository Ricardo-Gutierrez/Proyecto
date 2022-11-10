import time
from multiprocessing import Pool
import logging
import cv2 as cv
import os

# Relative path to the images
REL = "proyecto\\"

# debugging print format
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
)


def process_image(filename, threshold):  # Function to be executed in parallel
    process_id = str(os.getpid()).zfill(5)  # Get the process id
    # debugging print
    logging.debug(f'{process_id}: Processing {filename} - {threshold}')
    image = cv.imread(REL+filename)  # read image
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)  # convert to grayscale
    ret, thresh = cv.threshold(
        gray, threshold, 255, cv.THRESH_BINARY)  # threshold
    cv.imwrite(f'{REL}processed_{threshold}_{filename}', thresh)  # save image
    logging.debug(f'{process_id}: Finished {filename} - {threshold}')


if __name__ == '__main__':
    p = Pool()  # Create a multiprocessing Pool with 8 processes (8 cores)
    for thresh in range(0, 255, 5):  # for each threshold
        # apply the function to the image
        p.apply_async(process_image, args=(f'image.jpg', thresh))
    p.close()  # close the pool
    p.join()  # wait for all processes to finish