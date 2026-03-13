package dark;

import com.sun.jna.Pointer;
import com.sun.jna.Structure;

import java.util.Arrays;
import java.util.List;
/*
struct bbox_t_container {
        bbox_t candidates[C_SHARP_MAX_OBJECTS];
        };
 */
public class bbox_t_container extends Structure implements Structure.ByReference {
    public bbox_t[] candidates = new bbox_t[1000];

    public bbox_t_container() {
        super();
    }

    public bbox_t_container(Pointer peer) {
        super(peer);
    }

    @Override
    protected List<String> getFieldOrder() {
        return Arrays.asList("candidates");
    }
}