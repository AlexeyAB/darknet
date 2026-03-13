package dark;

import com.sun.jna.Pointer;
import com.sun.jna.Structure;
import java.util.Arrays;
import java.util.List;

public class image extends Structure implements Structure.ByValue {
    public int w;
    public int h;
    public int c;
    public Pointer data;

    public image() {
        super();
    }

    public image(Pointer peer) {
        super(peer);
    }

    @Override
    protected List<String> getFieldOrder() {
        return Arrays.asList("w","h","c","data");
    }
}