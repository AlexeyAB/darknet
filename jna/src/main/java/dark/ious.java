package dark;

import com.sun.jna.Pointer;
import com.sun.jna.Structure;

import java.util.Arrays;
import java.util.List;

public class ious extends Structure {
    public float iou, giou, diou, ciou;
    public dxrep dx_iou;
    public dxrep dx_giou;

    public ious() {
        super();
    }

    public ious(Pointer peer) {
        super(peer);
    }

    @Override
    protected List<String> getFieldOrder() {
        return Arrays.asList("iou", "giou", "diou", "ciou", "dx_iou", "dxrep", "dx_giou");
    }
}
