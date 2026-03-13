package dark;

import com.sun.jna.Pointer;
import com.sun.jna.Structure;

import java.util.Arrays;
import java.util.List;

        //box bbox;0
        //int classes;16
        //float *prob;24
        //float *mask;32
        //float objectness;36
        //int sort_class;40
        //float *uc; // Gaussian_YOLOv3 - tx,ty,tw,th uncertainty 48
        //int points; // bit-0 - center, bit-1 - top-left-corner, bit-2 - bottom-right-corner 52

public class detection extends Structure   {

    public box.ByValue bbox;//16 (float, float, float,float) (4x4 bytes)16
    public int classes;//20 (4 bytes)
    public Pointer prob;//28 (8 bytes)
    public Pointer mask;//36 ((8 bytes)
    public float objectness; //40 (4 bytes)
    public int sort_class; //44 (4 bytes)
    public Pointer uc;//float // Gaussian_YOLOv3 - tx,ty,tw,th uncertainty //52 (8 bytes)
    public int points; // bit-0 - center, bit-1 - top-left-corner, bit-2 - bottom-right-corner //56 (4 bytes)
    //60 + 4

    public detection() {
        super();
    }

    public detection(Pointer peer) {
        // cannot use super(p) because of fixed-size array fields
        super();
        useMemory(peer); // set pointer
        read(); // initialize fields
    }

    public detection(box bbox,int classes){

    }


    @Override
    protected List<String> getFieldOrder() {
        return Arrays.asList("bbox", "classes", "prob", "mask", "objectness", "sort_class", "uc", "points");
    }


    public static class ByReference extends detection implements Structure.ByReference {
        public ByReference() { }
        public ByReference(Pointer p) { super(p); read(); }
    }

}