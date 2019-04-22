# STEP 0 / OPTIONAL
# USAGE
# python face_recognition_dataset.py --detector face_detection_model  --output dataset/angie

import argparse
import os
import time
import cv2 as cv
import imutils
from imutils.video import VideoStream
import numpy as np


# face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--detector", required=True, help="path to OpenCV's deep learning face detector")
ap.add_argument("-o", "--output", required=True, help="path to output directory")
ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probability to filter weak detections")
args = vars(ap.parse_args())


# load our serialized face detector from disk
print("[INFO] loading face detector...")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"], "res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv.dnn.readNetFromCaffe(protoPath, modelPath)

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
    frame = imutils.resize(frame, width=600)
    (h, w) = frame.shape[:2]

    # construct a blob from the image
    imageBlob = cv.dnn.blobFromImage(
        cv.resize(frame, (300, 300)), 1.0, (300, 300),
        (104.0, 177.0, 123.0), swapRB=False, crop=False)

    # apply OpenCV's deep learning-based face detector to localize
    # faces in the input image
    detector.setInput(imageBlob)
    detections = detector.forward()

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections
        if confidence > args["confidence"]:
            # compute the (x, y)-coordinates of the bounding box for
            # the face
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # extract the face ROI
            face = frame[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]

            # ensure the face width and height are sufficiently large
            if fW < 20 or fH < 20:
                continue

            # construct a blob for the face ROI, then pass the blob
            # through our face embedding model to obtain the 128-d
            # quantification of the face
            faceBlob = cv.dnn.blobFromImage(face, 1.0 / 255,
                                             (96, 96), (0, 0, 0), swapRB=True, crop=False)

            cv.rectangle(frame, (startX, startY), (endX, endY),
                          (0, 0, 255), 2)


    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # # detect faces in the grayscale frame
    # rects = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    #
    # # loop over the face detections and draw them on the frame
    # for (x, y, w, h) in rects:
    #     cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

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

    # if the `q` key was pressed, break from the loop
    elif key == ord("q"):
        break

# print the total faces saved and do a bit of cleanup
print("[INFO] {} face images stored".format(total))
print("[INFO] cleaning up...")
cv.destroyAllWindows()
vs.stop()
