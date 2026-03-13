package dark;

import com.sun.jna.Native;
import com.sun.jna.Pointer;
import com.sun.jna.ptr.IntByReference;
import org.bytedeco.opencv.opencv_core.Mat;


import java.io.File;

import static java.lang.System.out;
import static org.bytedeco.opencv.global.opencv_imgcodecs.imread;


public class App
{
    network net;
    metadata meta;
    String[] altNames;
    //DarknetLib darknet = (DarknetLib) Native.load(new File(".").getAbsolutePath()+"/libdark.so", DarknetLib.class);
    DarknetLib darknet = (DarknetLib) Native.load(new File(".").getAbsolutePath()+"/dark.dll", DarknetLib.class);

    public static void main( String[] args ) {
        detection[] detections = new App().PerformDetect("data/dog.jpg",0.25f,"./cfg/yolov3.cfg","./cfg/yolov3.weights", "./cfg/coco.data",false);
    }

    App(){
    }

    App(String cfgFile,String weightsFile,String classesFile){
        PerformDetect(null,0,"./cfg/yolov3.cfg","./cfg/yolov3.weights", "./cfg/coco.data",true);
    }

    public detection[]  Detect(String filename, float thresh, float hier_thresh, float nms) {
        image im = darknet.load_image_color(filename, 0, 0);
        Mat mat = imread(filename);

        detection[] ret = DetectImage(im, thresh, hier_thresh, nms);

        Util.showImage(mat);
        darknet.free_image(im);
        return ret;
    }

    public detection[] DetectImage(image im, float thresh, float hier_thresh, float nms) {
        IntByReference pnum = new IntByReference(0);
        float pre = darknet.network_predict_image(net, im);
        int letter_box = 0;
        int map = 0;
        IntByReference pmap = new IntByReference(map);
        Pointer p =  darknet.get_network_boxes(net, im.w, im.h, thresh, hier_thresh, pmap, 0, pnum, letter_box);
        int num = pnum.getValue();
        detection det = new detection(p);
        if (nms>0) {
            darknet.do_nms_sort(det, num, meta.classes, nms);
        }
        detection[] detections = (detection[])det.toArray(num);
        for(int j=0;j<num;j++) {
            detection detect = detections[j];
            float[] probabilites = detect.prob.getFloatArray(0,meta.classes);
            for (int i = 0; i < meta.classes; i++) {
                if (probabilites[i] > 0) {
                    String nameTag = altNames[i];
                    //out.println("name:"+nameTag+"("+probabilites[i]+")");
                }
            }
        }
        darknet.free_detections(p, num);
        return detections;
    }

    public  detection[] PerformDetect(String imagePath,float thresh,String  configPath,String  weightPath,String  metaPath,boolean initOnly){
        if(0 < thresh && thresh > 1) {
            out.println("Threshold should be a float between zero and one (non-inclusive)");
        }
        if(! new File(configPath).exists()) {
            out.println("Invalid config path `"+ new File(configPath).getAbsolutePath()+"`");
        }
        if(!new File(weightPath).exists()) {
            out.println("Invalid weight path `"+new File(weightPath).getAbsolutePath()+"`");
        }
        if(!new File(metaPath).exists()) {
            out.println("Invalid meta path `"+new File(metaPath).getAbsolutePath()+"`");
        }
        if(net == null) {
            net = darknet.load_network_custom(configPath,weightPath, 0, 1);//  #batch size = 1
        }
        if(meta == null) {
            meta = darknet.get_metadata(metaPath);
        }
        if(altNames==null) {
            altNames = meta.names.getStringArray(0, meta.classes);
        }
        if(initOnly) {
            out.println("Initialized detector");
            return null;
        }
        float hier_thresh=.5f;
        float nms=.45f;
        detection[] detections = Detect(imagePath, thresh,hier_thresh,nms);
        int success = darknet.dispose();
        return detections;
    }
}