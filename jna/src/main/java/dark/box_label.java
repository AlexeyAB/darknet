package dark;

import com.sun.jna.Pointer;
import com.sun.jna.Structure;

import java.util.Arrays;
import java.util.List;

public class box_label extends Structure {
    public int id;
    public float x, y, w, h;
    public float left, right, top, bottom;

    public box_label() {
        super();
    }

    public box_label(Pointer peer) {
        super(peer);
    }

    @Override
    protected List<String> getFieldOrder() {
        return Arrays.asList("id","x","y","w","h","left","right","top","bottom");
    }
}
