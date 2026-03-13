#ifndef STREAM_H
#define STREAM_H

#include "image.h"
#ifdef __cplusplus
extern "C" {
#endif

void stream(char *cfgfile, char *weightfile, float thresh, float hier_thresh, int cam_index, const char *filename, char **names, int classes, int avgframes,
    int frame_skip, char *prefix, char *out_filename, int mjpeg_port, int dontdraw_bbox, int json_port, int dont_show, int ext_output, int letter_box_in, int time_limit_sec, char *http_post_host,
    int benchmark, int benchmark_layers,
    int stream_bitrate, char *dst_stream_addr, int dst_frame_width, int dst_frame_height, char *stream_profile, int stream_gop_size, int stream_fps);

#ifdef __cplusplus
}
#endif

#endif
