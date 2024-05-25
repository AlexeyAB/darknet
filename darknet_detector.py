#!python3
"""
Python 3 wrapper for identifying objects in images

Requires DLL compilation

Both the GPU and no-GPU version should be compiled; the no-GPU version should
be renamed "yolo_cpp_dll_nogpu.dll".

On a GPU system, you can force CPU evaluation by any of:

- Set global variable DARKNET_FORCE_CPU to True
- Set environment variable CUDA_VISIBLE_DEVICES to -1
- Set environment variable "FORCE_CPU" to "true"


To use, either run performDetect() after import, or modify the end of this
file.

See the docstring of performDetect() for parameters.

Directly viewing or returning bounding-boxed images requires scikit-image to be
installed (`pip install scikit-image`)

@author: Philip Kahn
@date: 20180503
"""
from ctypes import (
        CDLL, Structure, c_float, c_int, POINTER, c_char_p, RTLD_GLOBAL,
        c_void_p, pointer)
import os
import cv2
import numpy as np

"""
def sample(probs):
    s = sum(probs)
    probs = [a/s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs)-1

def c_array(ctype, values):
    arr = (ctype*len(values))()
    arr[:] = values
    return arr

"""


class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]


class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int),
                ("uc", POINTER(c_float)),
                ("points", c_int)]


class DETNUMPAIR(Structure):
    _fields_ = [("num", c_int),
                ("dets", POINTER(DETECTION))]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]


class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]


class Detector():

    def network_width(self, net):
        return self.lib.network_width(net)

    def network_height(self, net):
        return self.lib.network_height(net)

    def __init__(self, dll_path, configPath, weightPath, dataPath, labelsPath):
        """
            dll_path: str
                should be where libdarknet.so lives.

            configPath: str
                Path to the configuration file. Raises ValueError if not found

            weightPath: str
                Path to the weights file. Raises ValueError if not found

            dataPath: str
                Path to the data file. Raises ValueError if not found

            labelsPath: str
                Path to labels file

        """
        self.hasGPU = True
        self.lib = CDLL(dll_path, RTLD_GLOBAL)

        self.lib.network_width.argtypes = [c_void_p]
        self.lib.network_width.restype = c_int
        self.lib.network_height.argtypes = [c_void_p]
        self.lib.network_height.restype = c_int

        self.copy_image_from_bytes = self.lib.copy_image_from_bytes
        self.copy_image_from_bytes.argtypes = [IMAGE, c_char_p]

        self.predict = self.lib.network_predict_ptr
        self.predict.argtypes = [c_void_p, POINTER(c_float)]
        self.predict.restype = POINTER(c_float)

        if self.hasGPU:
            self.set_gpu = self.lib.cuda_set_device
            self.set_gpu.argtypes = [c_int]

        # init_cpu = self.lib.init_cpu

        self.make_image = self.lib.make_image
        self.make_image.argtypes = [c_int, c_int, c_int]
        self.make_image.restype = IMAGE

        self.get_network_boxes = self.lib.get_network_boxes
        self.get_network_boxes.argtypes = [
            c_void_p,
            c_int,
            c_int,
            c_float,
            c_float,
            POINTER(c_int),
            c_int,
            POINTER(c_int),
            c_int]
        self.get_network_boxes.restype = POINTER(DETECTION)

        self.make_network_boxes = self.lib.make_network_boxes
        self.make_network_boxes.argtypes = [c_void_p]
        self.make_network_boxes.restype = POINTER(DETECTION)

        self.free_detections = self.lib.free_detections
        self.free_detections.argtypes = [POINTER(DETECTION), c_int]

        self.free_batch_detections = self.lib.free_batch_detections
        self.free_batch_detections.argtypes = [POINTER(DETNUMPAIR), c_int]

        self.free_ptrs = self.lib.free_ptrs
        self.free_ptrs.argtypes = [POINTER(c_void_p), c_int]

        self.network_predict = self.lib.network_predict_ptr
        self.network_predict.argtypes = [c_void_p, POINTER(c_float)]

        self.reset_rnn = self.lib.reset_rnn
        self.reset_rnn.argtypes = [c_void_p]

        self.load_net = self.lib.load_network
        self.load_net.argtypes = [c_char_p, c_char_p, c_int]
        self.load_net.restype = c_void_p

        self.load_net_custom = self.lib.load_network_custom
        self.load_net_custom.argtypes = [c_char_p, c_char_p, c_int, c_int]
        self.load_net_custom.restype = c_void_p

        self.do_nms_obj = self.lib.do_nms_obj
        self.do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

        self.do_nms_sort = self.lib.do_nms_sort
        self.do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

        self.free_image = self.lib.free_image
        self.free_image.argtypes = [IMAGE]

        self.letterbox_image = self.lib.letterbox_image
        self.letterbox_image.argtypes = [IMAGE, c_int, c_int]
        self.letterbox_image.restype = IMAGE

        self.load_meta = self.lib.get_metadata
        self.lib.get_metadata.argtypes = [c_char_p]
        self.lib.get_metadata.restype = METADATA

        self.load_image = self.lib.load_image_color
        self.load_image.argtypes = [c_char_p, c_int, c_int]
        self.load_image.restype = IMAGE

        self.rgbgr_image = self.lib.rgbgr_image
        self.rgbgr_image.argtypes = [IMAGE]

        self.predict_image = self.lib.network_predict_image
        self.predict_image.argtypes = [c_void_p, IMAGE]
        self.predict_image.restype = POINTER(c_float)

        self.predict_image_letterbox = self.lib.network_predict_image_letterbox
        self.predict_image_letterbox.argtypes = [c_void_p, IMAGE]
        self.predict_image_letterbox.restype = POINTER(c_float)

        self.network_predict_batch = self.lib.network_predict_batch
        self.network_predict_batch.argtypes = [
            c_void_p,
            IMAGE,
            c_int,
            c_int,
            c_int,
            c_float,
            c_float,
            POINTER(c_int),
            c_int,
            c_int]
        self.network_predict_batch.restype = POINTER(DETNUMPAIR)

        if not os.path.exists(configPath):
            raise ValueError("Invalid config path `" +
                             os.path.abspath(configPath) + "`")
        if not os.path.exists(weightPath):
            raise ValueError("Invalid weight path `" +
                             os.path.abspath(weightPath) + "`")
        if not os.path.exists(dataPath):
            raise ValueError("Invalid data file path `" +
                             os.path.abspath(dataPath) + "`")

        self.net = self.load_net_custom(configPath.encode(
            "ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
        self.meta = self.load_meta(dataPath.encode("ascii"))

        # In Python 3, the metafile default access craps out on Windows (but
        # not Linux) Read the names file and create a list to feed to detect

        self.labels = open(labelsPath).read().strip().split("\n")
        self.altNames = [x.strip() for x in self.labels]
        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        self.COLOURS = np.random.randint(0, 255, size=(len(self.labels), 3),
                                         dtype="uint8")
        print("Initialized detector")

    def run_object_detector(
            self,
            image,
            obj_name,
            thresh=.5,
            hier_thresh=.5,
            nms=.45,
            debug=False,
            show_image=False):

        print("***** using darknet_detector (" + obj_name + ") *****")
        im = self.load_image(image.encode("ascii"), 0, 0)
        num = c_int(0)
        if debug:
            print("Assigned num")
        pnum = pointer(num)
        if debug:
            print("Assigned pnum")
        self.predict_image(self.net, im)
        letter_box = 0
        if debug:
            print("did prediction")
        dets = self.get_network_boxes(
            self.net,
            im.w,
            im.h,
            thresh,
            hier_thresh,
            None,
            0,
            pnum,
            letter_box)
        if debug:
            print("Got dets")
        num = pnum[0]
        if debug:
            print("got zeroth index of pnum")
        if nms:
            self.do_nms_sort(dets, num, self.meta.classes, nms)
        if debug:
            print("did sort")
        if debug:
            print("about to range")
        boxes = []
        confidences = []
        classIDs = []
        cropped_images = []
        cv_img = cv2.imread(image)

        for j in range(num):
            if debug:
                print("Ranging on " + str(j) + " of " + str(num))
            if debug:
                print("Classes: " + str(self.meta),
                      self.meta.classes, self.meta.names)
            for i in range(self.meta.classes):
                if debug:
                    print("Class-ranging on " + str(i) + " of " +
                          str(self.meta.classes) + "= " + str(dets[j].prob[i]))
                if dets[j].prob[i] > 0:
                    b = dets[j].bbox
                    if self.altNames is None:
                        nameTag = self.meta.names[i]
                    else:
                        nameTag = self.altNames[i]
                    if debug:
                        print("Got bbox", b)
                        print(nameTag)
                        print(dets[j].prob[i])
                        print((b.x, b.y, b.w, b.h))
                    boxes.append([b.x, b.y, b.w, b.h])
                    confidences.append(dets[j].prob[i])
                    classIDs.append(i)
                    (x, y, w, h) = self.bounding_box((b.x, b.y, b.w, b.h))
                    color = [int(c) for c in self.COLOURS[i]]
                    cv2.rectangle(cv_img, (x, y), (x + w, y + h), color, 2)
                    text = "{}".format(self.labels[i])
                    cv2.putText(cv_img, text, (x, y - 5),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, color, 2)
                    cropped = cv_img[y:y+h, x:x+w]
                    vname = obj_name + "_" + \
                        str(i) + "_" + nameTag + "_" + str(dets[j].prob[i])
                    cropped_images.append((cropped, vname))
        if debug:
            print("did range")
        if debug:
            print("did sort")
        self.free_detections(dets, num)
        if debug:
            print("freed detections")
        if show_image:
            cv2.imshow("image", cv_img)
            cv2.waitKey(0)
        return (boxes, confidences, classIDs, cropped_images)

    def bounding_box(self, bounds):
        yExtent = int(bounds[3])
        xExtent = int(bounds[2])
        # Coordinates are around the center
        xCoord = int(bounds[0] - bounds[2] / 2)
        yCoord = int(bounds[1] - bounds[3] / 2)
        """
        boundingBox = [
            [xCoord, yCoord],
            [xCoord, yCoord + yExtent],
            [xCoord + xEntent, yCoord + yExtent],
            [xCoord + xEntent, yCoord]
        ]
        """
        return (xCoord, yCoord, xExtent, yExtent)

    def performDetect(
            self,
            imagePath,
            thresh=0.25,
            show_image=True,
            makeImageOnly=False):
        """
        Convenience function to handle the detection and returns of objects.

        Displaying bounding boxes requires libraries scikit-image and numpy

        Parameters
        ----------------
        imagePath: str
            Path to the image to evaluate. Raises ValueError if not found

        thresh: float (default= 0.25)
            The detection threshold

        show_image: bool (default= True)
            Compute (and show) bounding boxes. Changes return.

        makeImageOnly: bool (default= False)
            If showImage is True, this won't actually *show* the image,
            but will create the array and return it.


       """
        (boxes, confidences, classIDs, croppedImages) =\
            self.run_object_detector(imagePath, "test_img", thresh=thresh,
                                     show_image=show_image)

        return boxes

    def performBatchDetect(
            self,
            thresh=0.25,
            hier_thresh=.5,
            nms=.45,
            batch_size=3):
        # NB! Image sizes should be the same
        # You can change the images, yet, be sure that they have the same width
        # and height
        img_samples = ['data/person.jpg', 'data/person.jpg', 'data/person.jpg']
        image_list = [cv2.imread(k) for k in img_samples]

        pred_height, pred_width, c = image_list[0].shape
        net_width, net_height = (
            self.network_width(self.net), self.network_height(self.net))
        img_list = []
        for custom_image_bgr in image_list:
            custom_image = cv2.cvtColor(custom_image_bgr, cv2.COLOR_BGR2RGB)
            custom_image = cv2.resize(
                custom_image, (net_width, net_height),
                interpolation=cv2.INTER_NEAREST)
            custom_image = custom_image.transpose(2, 0, 1)
            img_list.append(custom_image)

        arr = np.concatenate(img_list, axis=0)
        arr = np.ascontiguousarray(arr.flat, dtype=np.float32) / 255.0
        data = arr.ctypes.data_as(POINTER(c_float))
        im = IMAGE(net_width, net_height, c, data)

        batch_dets = self.network_predict_batch(
            self.net,
            im,
            batch_size,
            pred_width,
            pred_height,
            thresh,
            hier_thresh,
            None,
            0,
            0)
        batch_boxes = []
        batch_scores = []
        batch_classes = []
        for b in range(batch_size):
            num = batch_dets[b].num
            dets = batch_dets[b].dets
            if nms:
                self.do_nms_obj(dets, num, self.meta.classes, nms)
            boxes = []
            scores = []
            classes = []
            for i in range(num):
                det = dets[i]
                score = -1
                label = None
                for c in range(det.classes):
                    p = det.prob[c]
                    if p > score:
                        score = p
                        label = c
                if score > thresh:
                    box = det.bbox
                    left, top, right, bottom = map(
                        int, (box.x - box.w / 2, box.y - box.h / 2,
                              box.x + box.w / 2, box.y + box.h / 2))
                    boxes.append((top, left, bottom, right))
                    scores.append(score)
                    classes.append(label)
                    boxColor = (int(255 * (1 - (score ** 2))),
                                int(255 * (score ** 2)), 0)
                    cv2.rectangle(image_list[b], (left, top),
                                  (right, bottom), boxColor, 2)
            cv2.imwrite(os.path.basename(img_samples[b]), image_list[b])

            batch_boxes.append(boxes)
            batch_scores.append(scores)
            batch_classes.append(classes)
        self.free_batch_detections(batch_dets, batch_size)
        return batch_boxes, batch_scores, batch_classes


if __name__ == "__main__":
    detector = Detector("./libdarknet.so", "./cfg/yolov4.cfg",
                        "yolov4.weights", "./cfg/coco.data",
                        "./cfg/coco.names")
    detector.performDetect("./data/car.jpg", 0.25)
    detector = Detector("./libdarknet.so", "./cfg/yolov4.cfg",
                        "yolov4.weights", "./cfg/coco.data",
                        "./cfg/coco.names")
    detector.performDetect("./data/dog.jpg", 0.25)
