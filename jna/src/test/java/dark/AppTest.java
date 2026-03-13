package dark;

import com.sun.jna.Native;
import com.sun.jna.Pointer;
import com.sun.jna.platform.linux.XAttr;
import com.sun.jna.ptr.IntByReference;
import org.junit.Ignore;
import org.junit.Test;
import java.io.File;
import java.nio.ByteBuffer;
import static java.lang.System.out;
import static org.junit.Assert.assertTrue;

public class AppTest  {
    DarknetLib darknet = (DarknetLib) Native.load(new File(".").getAbsolutePath()+"/dark.dll", DarknetLib.class);
    int h = 576;
    int w = 768;
    int c = 3;
    int size = h*w*c;
    float hier_thresh=.5f;
    float nms=.45f;
    float thresh = .25f;

    @Test
    @Ignore
    public void testApp()
    {
        assertTrue( true );
    }

    @Test
    @Ignore
    public void testLoadNetworkBatch1(){
        network net = darknet.load_network("./cfg/yolov3.cfg","./cfg/yolov3.weights",0, 1);// # batch size = 1
        int success = darknet.dispose();
    }

    @Test
    @Ignore
    public void testLoadNetwork(){
        network net = darknet.load_network("./cfg/yolov3.cfg","./cfg/yolov3.weights",0);
        int success = darknet.dispose();
    }

    @Test
    @Ignore
    public void testLoadNetworkCustom(){
        network net = darknet.load_network_custom("./cfg/yolov3.cfg","./cfg/yolov3.weights",0,1);
        int success = darknet.dispose();
    }

    @Test
    @Ignore
    public void testNetworkWidth(){
        network net = darknet.load_network("./cfg/yolov3.cfg","./cfg/yolov3.weights",0, 1);// # batch size = 1
        int netWidth = darknet.network_width(net);
        assertTrue(netWidth == 416);
        int success = darknet.dispose();
    }

    @Test
    @Ignore
    public void testNetworkHeight(){
        network net = darknet.load_network("./cfg/yolov3.cfg","./cfg/yolov3.weights",0, 1);// # batch size = 1
        int netHeight = darknet.network_height(net);
        assertTrue(netHeight == 416);
        int success = darknet.dispose();
    }

    @Test
    @Ignore
    public void testInitCpu(){
        darknet.init_cpu();
    }

    @Test
    @Ignore
    public void testGetMetaData(){
        metadata meta = darknet.get_metadata("./cfg/coco.data");
        assertTrue(meta.classes==80);
    }

    @Test
    @Ignore
    public void testLetterBoxImage(){
        image im = darknet.load_image_color("./data/dog.jpg",w,h);
        image lbIm = darknet.letterbox_image(im,w,h);
        darknet.free_image(im);
        darknet.free_image(lbIm);
    }

    @Test
    @Ignore
    public void testCopyImageFromBytes(){
        //void copy_image_from_bytes(image im, Pointer pdata);
    }


    @Test
    @Ignore
    public void testResizeImage(){
        image im = darknet.load_image_color("./data/dog.jpg",w,h);
        image resized = darknet.resize_image(im,416,416);
        assertTrue(resized.h == 416);
        assertTrue(resized.w == 416);
        assertTrue(resized.c == c);
    }

    @Test
    @Ignore
    public void testLoadColorImage(){
        image im = darknet.load_image_color("./data/dog.jpg",w,h);
        assertTrue(im.w == w);
        assertTrue(im.h == h);
        assertTrue(im.c == c);
        darknet.free_image(im);
    }

    @Test
    @Ignore
    public void testMakeImage(){
        image im = darknet.make_image(100,50,3);
        assertTrue(im.w == 100);
        assertTrue(im.h == 50);
        assertTrue(im.c == 3);
        darknet.free_image(im);
    }

    @Test
    @Ignore
    public void testRgbgrImage() {
        image im = darknet.load_image_color("./data/dog.jpg",w,h);
        darknet.rgbgr_image(im);
    }

    @Test
    @Ignore
    public void testFreeImage(){
        image im = darknet.make_image(100,50,3);
        darknet.free_image(im);
    }

    @Test
    @Ignore
    public void testDeviceCount(){
        int deviceCnt = darknet.get_device_count();
    }

    @Test
    @Ignore
    public void testInitGpu0(){
        int deviceCnt = darknet.get_device_count();
        if(deviceCnt>0){
            int success = darknet.init("./cfg/yolov3.cfg","./cfg/yolov3.weights",0);
            assertTrue(success == 1);
            success = darknet.dispose();
            assertTrue(success == 1);
        }
    }

    @Test
    @Ignore
    public void testBuiltWithCuda(){
        boolean builtWithCuda = darknet.built_with_cuda();
    }

    @Test
    @Ignore
    public void testBuiltWithCudnn(){
        boolean builtWithCuda = darknet.built_with_cudnn();
    }

    @Test
    @Ignore
    public void testBuiltWithOpencv(){
        boolean builtWithCuda = darknet.built_with_opencv();
    }

    @Test
    @Ignore
    public void testGetDeviceName(){
        int deviceCnt = darknet.get_device_count();
        if(deviceCnt>0) {
            byte[] deviceName = new byte[256];
            int success =  darknet.get_device_name(0,deviceName);
            assertTrue(success == 1);
        }
    }

    @Test
    @Ignore
    public void testDetectImage(){
        int deviceCnt = darknet.get_device_count();
        if(deviceCnt>0){
            int success = darknet.init("./cfg/yolov3.cfg","./cfg/yolov3.weights",0);
            assertTrue(success == 1);
            bbox_t_container container = new bbox_t_container();
            success =  darknet.detect_image("./data/dog.jpg", container);//works
            bbox_t[] bbox_ts = container.candidates;
            assertTrue(bbox_ts[0].obj_id == 16);
            assertTrue(bbox_ts[1].obj_id == 7);
            assertTrue(bbox_ts[2].obj_id == 1);
            success = darknet.dispose();
            assertTrue(success == 1);

        }
    }

    @Test
    @Ignore
    public void testDispose(){
        int deviceCnt = darknet.get_device_count();
        if(deviceCnt>0){
            int success = darknet.init("./cfg/yolov3.cfg","./cfg/yolov3.weights",0);
            assertTrue(success == 1);
            success = darknet.dispose();
            assertTrue(success == 1);

        }
    }

    @Test
    @Ignore
    public void testDetectMat(){
        int deviceCnt = darknet.get_device_count();
        if(deviceCnt>0){
            int success = darknet.init("./cfg/yolov3.cfg","./cfg/yolov3.weights",0);
            assertTrue(success == 1);
            bbox_t_container container = new bbox_t_container();
            image im = darknet.load_image_color("./data/dog.jpg",w,h);
            XAttr.size_t data_length = new XAttr.size_t(size);
            ByteBuffer buf = ByteBuffer.allocate(size);
            //success = darknet.detect_mat(buf, data_length,  container);
            success = darknet.dispose();
            assertTrue(success == 1);
        }
    }

    @Test
    @Ignore
    public void testSendJsonCustom(){
        String send_buf = "";
        int port = 10101;
        //darknet.send_json_custom(send_buf, 10101, 5000);//not tested
    }

    @Test
    @Ignore
    public void testNetworkPredictImage(){
        network net = darknet.load_network_custom("./cfg/yolov3.cfg","./cfg/yolov3.weights",0,1);
        image im = darknet.load_image_color("./data/dog.jpg",w,h);
        float f = darknet.network_predict_image(net,im);
        darknet.free_image(im);
        int success = darknet.dispose();
        assertTrue(success == 1);
    }

    @Test
    public void testGetNetworkBoxes(){
        network net = darknet.load_network_custom("./cfg/yolov3.cfg","./cfg/yolov3.weights",0,1);
        int netH = darknet.network_height(net);
        assertTrue(netH == 416);
        int netW = darknet.network_width(net);
        assertTrue(netW == 416);
        metadata meta = darknet.get_metadata("./cfg/coco.data");
        String[] names = meta.names.getStringArray(0, meta.classes);
        image im = darknet.load_image_color("./data/dog.jpg",0,0);
        IntByReference pnum = new IntByReference(0);
        darknet.network_predict_image(net, im);
        Pointer p =  darknet.get_network_boxes(net, im.w, im.h, thresh, hier_thresh,  new IntByReference(0), 0, pnum, 0);
        int num = pnum.getValue();
        detection det = new detection(p);
        darknet.do_nms_sort(det, num, meta.classes, nms);
        detection[] detections = (detection[])det.toArray(num);
        for(int j=0;j<num;j++) {
            detection detect = detections[j];
            float[] probabilites = detect.prob.getFloatArray(0,meta.classes);
            for (int i = 0; i < meta.classes; i++) {
                if (probabilites[i] > 0) {
                    String nameTag = names[i];
                    out.println("name:"+nameTag+"("+probabilites[i]+")");
                }
            }
        }
        darknet.free_detections(p, num);
        darknet.free_image(im);
        int success = darknet.dispose();
        assertTrue(success == 1);
    }
    @Test
    @Ignore
    public void testDetectionToJson(){//FURTHER WORK REQUIRED - DOES NOT PASS
        network net = darknet.load_network_custom("./cfg/yolov3.cfg","./cfg/yolov3.weights",0,1);
        metadata meta = darknet.get_metadata("./cfg/coco.data");
        String[] names = meta.names.getStringArray(0, meta.classes);
        image im = darknet.load_image_color("./data/dog.jpg",0,0);
        IntByReference pnum = new IntByReference(0);
        darknet.network_predict_image(net, im);
        int num = pnum.getValue();
        Pointer p = darknet.get_network_boxes(net, im.w, im.h, thresh, hier_thresh,  new IntByReference(0), 0, pnum, 0);
        detection det = new detection(p);
        darknet.do_nms_sort(det, num, meta.classes, nms);
        detection[] detections = (detection[])det.toArray(num);
        String json = darknet.detection_to_json(det,num,meta.classes,names,0,null);
        darknet.free_detections(p, num);
        darknet.free_image(im);
        int success = darknet.dispose();
        assertTrue(success == 1);

    }
    @Test
    @Ignore
    public void makeNetworkBoxes(){//FURTHER WORK REQUIRED - DOES NOT PASS
        network net = darknet.load_network_custom("./cfg/yolov3.cfg","./cfg/yolov3.weights",0,1);
        metadata meta = darknet.get_metadata("./cfg/coco.data");
        String[] names = meta.names.getStringArray(0, meta.classes);
        image im = darknet.load_image_color("./data/dog.jpg",0,0);
        IntByReference pnum = new IntByReference(0);
        darknet.network_predict_image(net, im);
        int num = pnum.getValue();
        Pointer p = darknet.make_network_boxes(net,  thresh, pnum);
    }

    @Test
    public void getTimePoint(){
        double tp = darknet.get_time_point();
    }

    //**** box.h ***//
    //void do_nms_obj(detection dets, int total, int classes, float thresh);
    //void diounms_sort(detection dets, int total, int classes, float thresh, int nms_kind, float beta1);
    //**** network.h ***//
    //float network_predict(network net, FloatByReference input);
    //float network_predict_ptr(network net, FloatByReference input);
    //void fuse_conv_batchnorm(network net);
    //void calculate_binary_weights(network net);
    //void reset_rnn(network net);
    //float network_predict_image_letterbox(network net, image im);
    //float validate_detector_map(String datacfg,String cfgfile,String weightfile, float thresh_calc_avg_iou, float iou_thresh,int map_points, int letter_box, network existing_net);
    //void train_detector(String datacfg,String cfgfile, String weightfile, IntByReference gpus, int ngpus, int clear, int dont_show, int calc_map, int mjpeg_port, int show_imgs);
    //void test_detector(String datacfg,String cfgfile, String weightfile, String filename, float thresh, float hier_thresh, int dont_show, int ext_output, int save_labels, String outfile, int letter_box);
    //void optimize_picture(network net, image orig, int max_layer, float scale, float rate, float thresh, int norm);
    //**** layer.h ***//
    //void free_layer(layer lay);
    //**** data.c ***//
    //void free_data(data d);
    //void load_thread(Pointer ptr);
    //**** dark_cuda.h ***//
    //void cuda_pull_array(FloatByReference x_gpu, FloatByReference x, LongByReference n);
    //void cuda_pull_array_async(FloatByReference x_gpu, FloatByReference x, LongByReference n);
    //void cuda_set_device(int n);
    //void cuda_get_context();
    //**** utils.h ***//
    //void free_ptrs(PointerByReference ptrs, int n);
    //void top_k(FloatByReference a, int n, int k, IntByReference index);
    //**** tree.h ***//
    //tree read_tree(String filename);
    //**** http_stream.h ***//
    //void delete_json_sender();
    //void send_json_custom(byte[] send_buf, int port, int timeout);
}