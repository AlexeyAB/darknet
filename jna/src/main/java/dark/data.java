package dark;

import com.sun.jna.Pointer;
import com.sun.jna.Structure;
import com.sun.jna.ptr.PointerByReference;

import java.util.Arrays;
import java.util.List;

public class data extends Structure {
    int w;
    int h;
    matrix X;
    matrix Y;
    int shallow;
    Pointer num_boxes;
    PointerByReference boxes;
    public data() {
        super();
    }

    public data(Pointer peer) {
        super(peer);
    }

    @Override
    protected List<String> getFieldOrder() {
        return Arrays.asList("w","h","X","Y","shallow","num_boxes","boxes");
    }
}
// data.h
/*typedef struct data {
        int w, h;
        matrix X;
        matrix y;
        int shallow;
        int *num_boxes;
        box **boxes;
        } data;

 */