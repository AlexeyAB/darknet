package dark;

import com.sun.jna.Pointer;
import com.sun.jna.Structure;

import java.util.Arrays;
import java.util.List;

public class network_state extends Structure {
   public Pointer truth;
   public Pointer input;
   public Pointer delta;
   public Pointer workspace;
   public int train;
   public int index;
   public Pointer net;

   public network_state() {
      super();
   }

   public network_state(Pointer peer) {
      super(peer);
   }

   @Override
   protected List<String> getFieldOrder() {
      return Arrays.asList("truth","input","delta","workspace","train","index","net");
   }
}
/*
typedef struct network_state {
    float *truth;
    float *input;
    float *delta;
    float *workspace;
    int train;
    int index;
    network net;
} network_state;
 */