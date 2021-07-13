from ctypes import *
import random
import os
import cv2
import time
import darknet
import argparse
from threading import Thread, enumerate
from queue import Queue


class yolo_video():

    def __init__(self):
        self.cap = None

        self.args = None

        self.darknet_image = None

        self.width = None
        self.height = None

        self.network = None
        self.class_names = None
        self.class_colors = None

    def parser(self):
        parser = argparse.ArgumentParser(description="YOLO Object Detection")
        parser.add_argument("--input", type=str, default=0,
                            help="video source. If empty, uses webcam 0 stream")
        parser.add_argument("--out_filename", type=str, default="",
                            help="inference video name. Not saved if empty")
        parser.add_argument("--weights", default="yolov4.weights",
                            help="yolo weights path")
        parser.add_argument("--dont_show", action='store_true',
                            help="windown inference display. For headless systems")
        parser.add_argument("--ext_output", action='store_true',
                            help="display bbox coordinates of detected objects")
        parser.add_argument("--config_file", default="./cfg/yolov4.cfg",
                            help="path to config file")
        parser.add_argument("--data_file", default="./cfg/coco.data",
                            help="path to data file")
        parser.add_argument("--thresh", type=float, default=.25,
                            help="remove detections with confidence below this value")
        return parser.parse_args()

    def str2int(self, video_path):
        try:
            return int(video_path)
        except ValueError:
            return video_path

    def check_arguments_errors(self, args):
        assert 0 < self.args.thresh < 1, "Threshold should be a float between zero and one (non-inclusive)"
        if not os.path.exists(self.args.config_file):
            raise (ValueError("Invalid config path {}".format(os.path.abspath(self.args.config_file))))
        if not os.path.exists(self.args.weights):
            raise (ValueError("Invalid weight path {}".format(os.path.abspath(self.args.weights))))
        if not os.path.exists(self.args.data_file):
            raise (ValueError("Invalid data file path {}".format(os.path.abspath(self.args.data_file))))
        if self.str2int(self.args.input) == str and not os.path.exists(self.args.input):
            raise (ValueError("Invalid video path {}".format(os.path.abspath(self.args.input))))

    def set_saved_video(self, input_video, output_video, size):
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        fps = int(input_video.get(cv2.CAP_PROP_FPS))
        video = cv2.VideoWriter(output_video, fourcc, fps, size)
        return video

    def video_capture(self, frame_queue, darknet_image_queue):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (self.width, self.height),
                                       interpolation=cv2.INTER_LINEAR)
            frame_queue.put(frame_resized)
            darknet.copy_image_from_bytes(self.darknet_image, frame_resized.tobytes())
            darknet_image_queue.put(self.darknet_image)
        self.cap.release()

    def inference(self, darknet_image_queue, detections_queue, fps_queue):
        while self.cap.isOpened():
            self.darknet_image = darknet_image_queue.get()
            prev_time = time.time()
            detections = darknet.detect_image(self.network, self.class_names, self.darknet_image,
                                              thresh=self.args.thresh)
            detections_queue.put(detections)
            fps = int(1 / (time.time() - prev_time))
            fps_queue.put(fps)
            print("FPS: {}".format(fps))
            darknet.print_detections(detections, self.args.ext_output)
        self.cap.release()

    def drawing(self, frame_queue, detections_queue, fps_queue):
        random.seed(3)  # deterministic bbox colors
        video = self.set_saved_video(self.cap, self.args.out_filename, (self.width, self.height))
        while self.cap.isOpened():
            frame_resized = frame_queue.get()
            detections = detections_queue.get()
            fps = fps_queue.get()
            if frame_resized is not None:
                image = darknet.draw_boxes(detections, frame_resized, self.class_colors)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                print(detections)
                if self.args.out_filename is not None:
                    video.write(image)
                if not self.args.dont_show:
                    cv2.imshow('Inference', image)
                if cv2.waitKey(fps) == 27:
                    break
        self.cap.release()
        video.release()
        cv2.destroyAllWindows()

    def start(self):

        frame_queue = Queue()
        darknet_image_queue = Queue(maxsize=1)
        detections_queue = Queue(maxsize=1)
        fps_queue = Queue(maxsize=1)

        self.args = self.parser()
        self.check_arguments_errors(self.args)
        self.network, self.class_names, self.class_colors = darknet.load_network(
            self.args.config_file,
            self.args.data_file,
            self.args.weights,
            batch_size=1
        )
        self.width = darknet.network_width(self.network)
        self.height = darknet.network_height(self.network)
        self.darknet_image = darknet.make_image(self.width, self.height, 3)
        input_path = self.str2int(self.args.input)
        self.cap = cv2.VideoCapture(input_path)
        Thread(target=self.video_capture, args=(frame_queue, darknet_image_queue)).start()
        Thread(target=self.inference, args=(darknet_image_queue, detections_queue, fps_queue)).start()
        Thread(target=self.drawing, args=(frame_queue, detections_queue, fps_queue)).start()


demo = yolo_video()
demo.start()
