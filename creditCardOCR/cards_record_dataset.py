# USAGE
# python cards_record_dataset.py --output recordImages
import argparse
import os
import time
import cv2 as cv
import imutils
from imutils.video import VideoStream

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True, help="path to output directory")
args = vars(ap.parse_args())

# initialize the video stream, allow the camera sensor to warm up,
# and initialize the total number of example faces written to disk
# thus far
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
total = 0

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream, clone it, (just
    # in case we want to write it to disk), and then resize the frame
    # so we can apply face detection faster
    frame = vs.read()
    orig = frame.copy()
    frame = imutils.resize(frame, width=400)

    #show the output frame
    cv.imshow("Frame", frame)
    key = cv.waitKey(1) & 0xFF

    # if the `k` key was pressed, write the *original* frame to disk
    # so we can later process it and use it for face recognition
    if key == ord("k"):
        p = os.path.sep.join([args["output"], "{}.png".format(
            str(total).zfill(5))])
        cv.imwrite(p, orig)
        total += 1

    # if the `esc` key was pressed, break from the loop
    elif key == 27:
        break

# print the total faces saved and do a bit of cleanup
print("[INFO] {} cards images stored".format(total))
print("[INFO] cleaning up...")
cv.destroyAllWindows()
vs.stop()
