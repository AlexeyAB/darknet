package dark;

import com.sun.jna.Library;
import com.sun.jna.Pointer;
import com.sun.jna.ptr.FloatByReference;
import com.sun.jna.ptr.IntByReference;
import com.sun.jna.ptr.LongByReference;
import com.sun.jna.ptr.PointerByReference;

public interface DarknetLib extends Library, YoloV2_Lib {
    // parser.c
    network load_network(String configurationFilename, String weightsFilename, int clear, int batch);// # batch size = 1
    network load_network(String cfg,String weights, int clear);
    network load_network_custom(String cfg,String weights, int clear, int batch);//works
    // box.h
    void do_nms_sort(detection dets, int total, int classes, float thresh);//works
    void do_nms_obj(detection dets, int total, int classes, float thresh);
    void diounms_sort(detection dets, int total, int classes, float thresh, int nms_kind, float beta1);
    // network.h
    float network_predict(network net, FloatByReference input);
    float network_predict_ptr(network net, FloatByReference input);
    Pointer get_network_boxes(network net, int w, int h, float thresh, float hier,IntByReference map, int relative, IntByReference num, int letter);//works
    void free_detections(Pointer dets, int n);//works
    void fuse_conv_batchnorm(network net);
    void calculate_binary_weights(network net);
    String detection_to_json(detection dets, int nboxes, int classes,String[] names,long frame_id, String filename);
    Pointer make_network_boxes(network net, float thresh, IntByReference num);
    void reset_rnn(network net);
    float network_predict_image(network net, image im);//works
    float network_predict_image_letterbox(network net, image im);
    float validate_detector_map(String datacfg,String cfgfile,String weightfile, float thresh_calc_avg_iou, float iou_thresh,int map_points, int letter_box, network existing_net);
    void train_detector(String datacfg,String cfgfile, String weightfile, IntByReference gpus, int ngpus, int clear, int dont_show, int calc_map, int mjpeg_port, int show_imgs);
    void test_detector(String datacfg,String cfgfile, String weightfile, String filename, float thresh, float hier_thresh, int dont_show, int ext_output, int save_labels, String outfile, int letter_box);
    int network_width(network net);
    int network_height(network net);
    void optimize_picture(network net, image orig, int max_layer, float scale, float rate, float thresh, int norm);
    // image.h
    image resize_image(image im, int w, int h);
    void copy_image_from_bytes(image im, Pointer pdata);
    image letterbox_image(image im, int w, int h);
    void rgbgr_image(image im);
    image make_image(int w, int h, int c);
    image load_image_color(String filename, int w, int h);//works
    void free_image(image m);//works
    // layer.h
    void free_layer(layer lay);
    // data.c
    void free_data(data d);
    void load_thread(Pointer ptr);
    // dark_cuda.h
    void cuda_pull_array(FloatByReference x_gpu, FloatByReference x, LongByReference n);
    void cuda_pull_array_async(FloatByReference x_gpu, FloatByReference x, LongByReference n);
    void cuda_set_device(int n);
    void cuda_get_context();
    // utils.h
    void free_ptrs(PointerByReference ptrs, int n);
    void top_k(FloatByReference a, int n, int k, IntByReference index);
    // tree.h
    tree read_tree(String filename);
    // option_list.h
    metadata get_metadata(String file);
    // http_stream.h
    void delete_json_sender();
    void send_json_custom(byte[] send_buf, int port, int timeout);
    double get_time_point();
    // gemm.h
    void init_cpu();
}