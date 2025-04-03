package dark;

import com.sun.jna.Pointer;
import com.sun.jna.Structure;

import java.util.Arrays;
import java.util.List;

public class network extends Structure {
    public int n;
    public int batch;
    public Pointer seen;//uint64_t *seen;
    public Pointer t;//int *t;
    public float epoch;
    public int subdivisions;
    public Pointer layer;//layer *layers;
    public Pointer output;//float *output;
    public int polity;//learning_rate_policy policy;
    public float learning_rate;
    public float learning_rate_min;
    public float learning_rate_max;
    public int batches_per_cycle;
    public int batches_cycle_mult;
    public float momentum;
    public float decay;
    public float gamma;
    public float scale;
    public float power;
    public int time_steps;
    public int step;
    public int max_batches;
    public int num_boxes;
    public int train_images_num;
    public Pointer seq_scales; //float *seq_scales;
    public Pointer scales; //float *scales;
    public Pointer steps; //int   *steps;
    public int num_steps;
    public int burn_in;
    public int cudnn_half;
    public int adam;
    public float B1;
    public float B2;
    public float eps;
    public int inputs;
    public int outputs;
    public int truths;
    public int notruth;
    public int h;
    public int w;
    public int c;
    public int max_crop;
    public int min_crop;
    public float max_ratio;
    public float min_ratio;
    public int center;
    public int flip; // horizontal flip 50% probability augmentaiont for classifier training (default = 1)
    public int blur;
    public int mixup;
    public float label_smooth_eps;
    public int letter_box;
    public float angle;
    public float aspect;
    public float exposure;
    public float saturation;
    public float hue;
    public int random;
    public int track;
    public int augment_speed;
    public int sequential_subdivisions;
    public int init_sequential_subdivisions;
    public int current_subdivision;
    public int try_fix_nan;
    public int gpu_index;
    public Pointer hierarchy; //tree *hierarchy;
    public Pointer input;//float *input;
    public Pointer truth;//float *truth;
    public Pointer delta;//float *delta;
    public Pointer workspace;//float *workspace;
    public int train;
    public int index;
    public Pointer cost;//float *cost;
    public float clip;

    public network() {
        super();
    }

    public network(Pointer peer) {
        super(peer);
    }

    @Override
    protected List<String> getFieldOrder() {
        return Arrays.asList(
                "n",
                "batch",
                "seen",
                "t",
                "epoch",
                "subdivisions",
                "layer",
                "output",
                "polity",
                "learning_rate",
                "learning_rate_min",
                "learning_rate_max",
                "batches_per_cycle",
                "batches_cycle_mult",
                "momentum",
                "decay",
                "gamma",
                "scale",
                "power",
                "time_steps",
                "step",
                "max_batches",
                "num_boxes",
                "train_images_num",
                "seq_scales",
                "scales",
                "steps",
                "num_steps",
                "burn_in",
                "cudnn_half",
                "adam",
                "B1",
                "B2",
                "eps",
                "inputs",
                "outputs",
                "truths",
                "notruth",
                "h",
                "w",
                "c",
                "max_crop",
                "min_crop",
                "max_ratio",
                "min_ratio",
                "center",
                "flip",
                "blur",
                "mixup",
                "label_smooth_eps",
                "letter_box",
                "angle",
                "aspect",
                "exposure",
                "saturation",
                "hue",
                "random",
                "track",
                "augment_speed",
                "sequential_subdivisions",
                "init_sequential_subdivisions",
                "current_subdivision",
                "try_fix_nan",
                "gpu_index",
                "hierarchy",
                "input",
                "truth",
                "delta",
                "workspace",
                "train",
                "index",
                "cost",
                "clip"
        );
    }
}