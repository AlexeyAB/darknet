package dark;

import com.sun.jna.Pointer;
import com.sun.jna.Structure;

import java.nio.FloatBuffer;
import java.util.Arrays;
import java.util.List;

public class image_t extends Structure implements Structure.ByReference {
    public int h;                        // height
    public int w;                        // width
    public int c;                        // number of chanels (3 - for RGB)
    public FloatBuffer data;                  // pointer to the image data

    public image_t() {
        super();
    }

    public image_t(Pointer peer) {
        super(peer);
        read();
    }

    class ByReference extends image_t implements Structure.ByReference {
        public ByReference() { }
        public ByReference(Pointer p) { super(p); read(); }
    }


    public image_t(int h, int w, int c,FloatBuffer data){
        super();
        this.h = h;
        this.w = w;
        this.c = c;
        this.data = data;
    }
    @Override
    protected List<String> getFieldOrder() {
        return Arrays.asList("h","w","c","data");
    }


}
