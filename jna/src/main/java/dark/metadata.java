package dark;
import com.sun.jna.Pointer;
import com.sun.jna.Structure;

import java.util.Arrays;
import java.util.List;

public class metadata extends Structure implements Structure.ByValue {
    public int classes;
    public Pointer names;

    public metadata() {
        super();
    }

    public metadata(Pointer peer) {
        super(peer);
    }

    @Override
    protected List<String> getFieldOrder() {
        return Arrays.asList("classes","names");
    }
}
/*// option_list.h
typedef struct metadata {
    int classes;
    char **names;
} metadata;
*/