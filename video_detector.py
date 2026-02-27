#Import the neccesary libraries
import numpy as np
import argparse
import cv2 

# construct the argument parse 
parser = argparse.ArgumentParser(
    description='Script to run MobileNet-SSD object detection network ')
parser.add_argument("--video", help="path to video file. If empty, camera's stream will be used")
parser.add_argument("--config", default='cfg/yolov3.cfg', help="YOLO config path")
parser.add_argument("--weights", default='yolov3.weights', help="YOLO weights path")
parser.add_argument("--names", default='data/coco.names', help="class names path")

# parser.add_argument("--prototxt", default="MobileNetSSD_deploy.prototxt",
#                                   help='Path to text network file: '
#                                        'MobileNetSSD_deploy.prototxt for Caffe model or '
#                                        )
# parser.add_argument("--weights", default="MobileNetSSD_deploy.caffemodel",
#                                  help='Path to weights: '
#                                       'MobileNetSSD_deploy.caffemodel for Caffe model or '
#                                       )
# parser.add_argument("--thr", default=0.2, type=float, help="confidence threshold to filter out weak detections")
args = parser.parse_args()

CONF_THRESH, NMS_THRESH = 0.7, 0.7


# Open video file or capture device. 
if args.video:
    cap = cv2.VideoCapture(args.video)
else:
    cap = cv2.VideoCapture(0)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

fourcc = cv2.VideoWriter_fourcc(*'MPEG') # XVID')
out = cv2.VideoWriter("result.avi", fourcc, 20.0, (frame_width, frame_height)) # 640,480)) # avi


# Load the network
net = cv2.dnn.readNetFromDarknet(args.config, args.weights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Get the output layer from YOLO
layers = net.getLayerNames()
output_layers = [layers[i[0] - 1] for i in net.getUnconnectedOutLayers()]
print()
cnt = 0


total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(total)
while True:
    if cnt == total: # 5: # 10:
        break

    print('Processing frame %d' % cnt)
    # Capture frame-by-frame
    ret, frame = cap.read()
    height, width = frame.shape[:2]
    # frame_resized = cv2.resize(frame,(300,300)) # resize frame for prediction

    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), swapRB=True, crop=False)
    #Set to network the input blob 
    net.setInput(blob)
    #Prediction of network
    layer_outputs = net.forward(output_layers)


    class_ids, confidences, b_boxes = [], [], []
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > CONF_THRESH:
                center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                b_boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(int(class_id))

    # print('%d objects found\n' % len(b_boxes))
    if not len(b_boxes):
        out.write(frame)
        continue
    
    # Perform non maximum suppression for the bounding boxes to filter overlapping and low confident bounding boxes
    indices = cv2.dnn.NMSBoxes(b_boxes, confidences, CONF_THRESH, NMS_THRESH).flatten().tolist()

    # print('%d objects preserved after NMS\n' % len(indices))

    # Draw the filtered bounding boxes with their class to the image
    with open(args.names, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    for index in indices:
        x, y, w, h = b_boxes[index]
        print(x,y,w,h)
        cv2.rectangle(frame, (x, y), (x + w, y + h), 25, 2)
        cv2.putText(frame, classes[class_ids[index]], (x + 5, y + 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 25,2)
        print(x,y,w,h)
                    

    # cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    # cv2.imshow("frame", frame)
    out.write(frame)
    # cv2.imwrite('frame_%d.jpg' % cnt, frame)

    cnt += 1

out.release()
cap.release()