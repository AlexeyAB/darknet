package dark;

import com.sun.jna.Pointer;
import com.sun.jna.Structure;

import java.util.Arrays;
import java.util.List;

public class box extends Structure  implements Structure.ByValue{
    public float x;
    public float y;
    public float w;
    public float h;

    public box() {
        super();
    }

    public box(Pointer peer) {
        super(peer);
        read();
    }

    public box(float x,float y,float w,float h){
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
    }

    public box(float[] bbox){
        x = bbox[0];
        y = bbox[1];
        w = bbox[2];
        h = bbox[3];
    }

    @Override
    protected List<String> getFieldOrder() {
        return Arrays.asList("x","y","w","h");
    }

    public static class ByReference extends detection implements Structure.ByReference {
        public ByReference() { }
        public ByReference(Pointer p) { super(p); read(); }
    }

    public static class ByValue extends box implements Structure.ByValue { }
}