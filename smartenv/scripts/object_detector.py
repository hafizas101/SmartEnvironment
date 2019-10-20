#!/usr/bin/env python
# coding: utf-8
# In[8]:
from utils.logger import Logger
from queue import Queue
import numpy as np
import threading
import time
import cv2
import os

# In[9]:
# This class takes image parameter which should be a 3d numpy array and returns the list of objects detected in the image

class Object_Detector(threading.Thread, Logger):
    def __init__(self, img_q, response_q):
        threading.Thread.__init__(self)
        Logger.__init__(self, "YOLO")
        self.log("Intialized.")
        self.image_queue = img_q
        self.response_queue = response_q
        self.image = None

    def run(self):
        self.log("Starting YOLO detector ...")
        while 1:
            self.image = self.image_queue.get(block=True, timeout=None)
            res = self.process_image()
            self.response_queue.put(res, block=True)

    def process_image(self):
        confidence_t = 0.5
        threshold_t = 0.3

        labelsPath = os.path.join(os.getcwd(), "yolo_files/names.txt")
        LABELS = open(labelsPath).read().strip().split("\n")
        names = []
        np.random.seed(42)
        COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),dtype="uint8")
        weightsPath = os.path.join(os.getcwd(), "yolo_files/yolov3.weights")
        configPath = os.path.join(os.getcwd(), "yolo_files/yolov3.cfg")

        # image should be a 3d numpy array
        image = self.image
        (H, W) = image.shape[:2]

        # Let's apply Yolo dectector using pretrained weights
        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln)
        end = time.time()
        self.log("[INFO] YOLO took {:.6f} seconds".format(end - start))

        # Let us assign class labels to the objects from layerOutputs
        boxes = []
        confidences = []
        classIDs = []
        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                if confidence > confidence_t:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping bounding
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence_t,threshold_t)

        # Let's make output image and store class labels in a list
        if len(idxs) > 0:
            for i in idxs.flatten():
                names.append(LABELS[classIDs[i]])
        self.log("Detected objects: "+str(names))
        return names

