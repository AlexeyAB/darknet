package dark;


import org.bytedeco.javacpp.*;
import org.bytedeco.opencv.opencv_core.*;
import org.bytedeco.opencv.opencv_stitching.*;
import static org.bytedeco.opencv.global.opencv_core.*;
import static org.bytedeco.opencv.global.opencv_highgui.*;
import static org.bytedeco.opencv.global.opencv_imgcodecs.*;
import static org.bytedeco.opencv.global.opencv_stitching.*;

public class Util{
    static Mat getMat(byte[] bytes){
        return null;
    }

    static Mat getMat(image image){
        return null;
    }

    static Mat getMat(image_t image){
        return null;
    }

    static void showImage(Mat mat){
        namedWindow("Test");
        imshow("Test", mat);
        waitKey(0);
        destroyWindow("Test");
    }

    static void showImage(image image){
        namedWindow("Test");
        Mat mat = getMat(image);
        imshow("Test", mat);
        waitKey(0);
        destroyWindow("Test");
    }

    static void save(Mat mat,String fileName){
    }

    static Mat loadMat(String fileName){
        return null;
    }
}