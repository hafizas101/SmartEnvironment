import cv2 as cv
import queue
import apriltag
from utils.logger import Logger
import threading

class RobotTracker(threading.Thread, Logger):
    def __init__(self, img_q, trig_q, stream):
        threading.Thread.__init__(self)
        Logger.__init__(self, "ROBOT_TRACKER")
        self.log("Initializing.")
        self.image_queue = img_q
        self.trigger_queue = trig_q

        self.detector = apriltag.Detector()
        self.video_stream = stream
        self.window_name = "robot_win"
        self.stop_ = False
        self.target_id = 0
        self.ready = False
        self.was_ready = 0

    def find_cropsize(self, rect):      # rect (x, y, w, h),
        x_lt = rect[0] - 3*rect[2]
        y_lt = rect[1] - 1*rect[3]
        w = rect[2]*7
        h = rect[3]*3
        return (x_lt if x_lt>0 else 0, y_lt if y_lt>0 else 0, w, h)

    def run(self):
        self.log("Starting tracker ...")
        self.log(self.video_stream)
        self.stop_ = False

        window = cv.namedWindow(self.window_name, cv.WINDOW_NORMAL)
        cv.startWindowThread()

        video = cv.VideoCapture(self.video_stream)
        if not video.isOpened():
            self.log("Error: unable to open video stream.")

        while 1:
            if not self.trigger_queue.empty():
                data_ = self.trigger_queue.get(block=False)
                if data_["locate"] == True:
                    self.log("Locating tag {}".format(data_["tag_id"]))
                    self.ready = True
                    self.target_id = data_["tag_id"]
                    self.was_ready = 1
                elif data_["locate"] == False:
                    self.was_ready = 2
                    self.ready = False

            ok, frame = video.read()
            if not ok or frame is None:
                self.log("Error: Unable to read video stream.")
                break
            frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            if self.ready:
                tags = self.detector.detect(frame_gray)
                for tag in tags:    # show all tags
                    top_left = tag.corners[3]
                    bottom_right = tag.corners[1]

                    x_t, y_t = int(top_left[0]), int(top_left[1])
                    x_b, y_b = int(bottom_right[0]), int(bottom_right[1])

                    col = (255, 0, 0) if tag.tag_id == self.target_id else (0, 0, 255)
                    cv.rectangle(frame, (x_t, y_t), (x_b, y_b), col, 3)

                    if tag.tag_id == self.target_id:
                        im_height, im_width = frame_gray.shape
                        crs = self.find_cropsize((x_t, y_t, abs(x_b-x_t), abs(y_b-y_t)))
                        crop_img = frame[crs[1]:crs[1]+crs[3], crs[0]:crs[0]+crs[2]]
                        self.image_queue.put_nowait(crop_img)
                        cv.rectangle(frame_gray, (crs[0], crs[1]), (crs[0]+crs[2], crs[1]+crs[3]), col, 3)
                        self.log("Robot Tag Detected, tag_id: {}".format(tag.tag_id))
                        self.ready = False

            cv.imshow(self.window_name, frame)
            k = cv.waitKey(1) & 0xff
            if k==27:
                break

            if self.was_ready is 2:
                self.was_ready = 0
                self.log("Stoping robot location.")
                video.release()
                cv.destroyWindow(self.window_name)
                #cv.destroyAllwindows()
                cv.waitKey(10)
