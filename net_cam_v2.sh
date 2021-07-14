#rm test_dnn_out.avi

./darknet detector demo ./cfg/coco.data ./cfg/yolov2.cfg ./yolov2.weights rtsp://admin:admin12345@192.168.0.228:554 -i 0 -thresh 0.25



