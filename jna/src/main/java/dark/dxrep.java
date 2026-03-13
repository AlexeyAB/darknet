package dark;

import com.sun.jna.Pointer;
import com.sun.jna.Structure;

import java.util.Arrays;
import java.util.List;

public class dxrep extends Structure {
    public float dt, db, dl, dr;

    public dxrep() {
        super();
    }

    public dxrep(Pointer peer) {
        super(peer);
    }

    @Override
    protected List<String> getFieldOrder() {
        return Arrays.asList("dt","db","dl","dr");
    }
}