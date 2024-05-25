package dark;

import com.sun.jna.Pointer;
import com.sun.jna.Structure;
import com.sun.jna.ptr.PointerByReference;

import java.util.Arrays;
import java.util.List;

public class matrix extends Structure {
    int rows;
    int cols;
    PointerByReference vals;
    public matrix() {
        super();
    }

    public matrix(Pointer peer) {
        super(peer);
    }

    @Override
    protected List<String> getFieldOrder() {
        return Arrays.asList("rows","cols","vals");
    }
}