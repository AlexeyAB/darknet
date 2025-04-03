#ifndef FFMPEG_H
#define FFMPEG_H

#include "image.h"
#include "matrix.h"

#ifdef __cplusplus
extern "C" {
#endif

#ifdef FFMPEG

void close_stream();
void av_pkt_unref();
void open_video_stream(const char *filename);
image get_image_from_ffmpeg_stream_resize(mat_cv** in_image, int w, int h, int c);

#endif

#ifdef __cplusplus
}
#endif

#endif  //FFMPEG_H
