package dark;

import com.sun.jna.Pointer;
import com.sun.jna.Structure;
import com.sun.jna.ptr.PointerByReference;

import java.util.Arrays;
import java.util.List;

public class load_args extends Structure implements Structure.ByValue {
    public int threads;
    public PointerByReference paths;
    public Pointer path;
    public int n;
    public int m;
    public PointerByReference labels;
    public int h;
    public int w;
    public int c; // color depth
    public int out_w;
    public int out_h;
    public int nh;
    public int nw;
    public int num_boxes;
    public int min, max, size;
    public int classes;
    public int background;
    public int scale;
    public int center;
    public int coords;
    public int mini_batch;
    public int track;
    public int augment_speed;
    public int letter_box;
    public int show_imgs;
    public float jitter;
    public int flip;
    public int blur;
    public int mixup;
    public float label_smooth_eps;
    public float angle;
    public float aspect;
    public float saturation;
    public float exposure;
    public float hue;
    public Pointer d;
    public Pointer im;
    public Pointer resized;
    public int type;
    public Pointer hierarchy;

    public load_args() {
        super();
    }

    public load_args(Pointer peer) {
        super(peer);
    }

    @Override
    protected List<String> getFieldOrder() {
        return Arrays.asList(
    "threads",
    "paths",
    "path",
    "n",
    "m",
    "labels",
    "h",
    "w",
    "c",
    "out_w",
    "out_h",
    "nh",
    "nw",
    "num_boxes",
    "min",
    "max",
    "size",
    "classes",
    "background",
    "scale",
    "center",
    "coords",
    "mini_batch",
    "track",
    "augment_speed",
    "letter_box",
    "show_imgs",
    "jitter",
    "flip",
    "blur",
    "mixup",
    "label_smooth_eps",
    "angle",
    "aspect",
    "saturation",
    "exposure",
    "hue",
    "d",
    "im",
    "resized",
    "type",
    "hierarchy");
    }
}
