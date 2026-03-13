package dark;

import com.sun.jna.Pointer;
import com.sun.jna.Structure;

import java.util.Arrays;
import java.util.List;

public class boxabs extends Structure {
    public float left,right,top,bot;

    public boxabs() {
        super();
    }

    public boxabs(Pointer peer) {
        super(peer);
    }

    @Override
    protected List<String> getFieldOrder() {
        return Arrays.asList("left","right","top","bot");
    }
}