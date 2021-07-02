package dark;

import com.sun.jna.Pointer;
import com.sun.jna.Structure;

import java.util.Arrays;
import java.util.List;
/*
struct bbox_t {
    unsigned int x, y, w, h;       // (x,y) - top-left corner, (w, h) - width & height of bounded box
    float prob;                    // confidence - probability that the object was found correctly
    unsigned int obj_id;           // class of object - from range [0, classes-1]
    unsigned int track_id;         // tracking id for video (0 - untracked, 1 - inf - tracked object)
    unsigned int frames_counter;   // counter of frames on which the object was detected
    float x_3d, y_3d, z_3d;        // center of object (in Meters) if ZED 3D Camera is used
};
 */
public class bbox_t extends Structure implements Structure.ByValue {
    public int x, y, w, h;       // (x,y) - top-left corner, (w, h) - width & height of bounded box
    public float prob;                    // confidence - probability that the object was found correctly
    public int obj_id;           // class of object - from range [0, classes-1]
    public int track_id;         // tracking id for video (0 - untracked, 1 - inf - tracked object)
    public int frames_counter;   // counter of frames on which the object was detected
    public float x_3d, y_3d, z_3d;        // center of object (in Meters) if ZED 3D Camera is used


    public bbox_t() {
        super();
    }

    public bbox_t(Pointer peer) {
        super(peer);
    }

    @Override
    protected List<String> getFieldOrder() {
        return Arrays.asList("x","y","w","h","prob","obj_id","track_id","frames_counter","x_3d","y_3d","z_3d");
    }
}