package dark;

import com.sun.jna.Library;
import com.sun.jna.platform.linux.XAttr;

import java.nio.ByteBuffer;

public interface YoloV2_Lib extends Library {
    int init(String configurationFilename, String weightsFilename, int gpu);//works
    int detect_image(String filename, bbox_t_container container);//works
    int detect_mat(ByteBuffer buf,  XAttr.size_t data_length, bbox_t_container container);//Still having issues passing ByteBuffer
    int dispose();//works
    int get_device_count();//works
    int get_device_name(int gpu,  byte[] deviceName);//works
    boolean built_with_cuda();//works
    boolean built_with_cudnn();//works
    boolean built_with_opencv();//works
    void send_json_custom(String send_buf, int port, int timeout);//not tested
}
