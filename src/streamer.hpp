// from https://github.com/andreanobile/opencv_ffmpeg_streaming
#ifndef STREAMER_HPP
#define STREAMER_HPP

#ifdef _WIN32
//Windows
extern "C" {
#include "libavutil/opt.h"
#include "libavcodec/avcodec.h"
#include "libavutil/channel_layout.h"
#include "libavutil/common.h"
#include "libavutil/imgutils.h"
#include "libavutil/mathematics.h"
#include "libavutil/samplefmt.h"

#include "libavformat/avformat.h"
#include "libavcodec/avcodec.h"
#include "libavutil/imgutils.h"
#include "libswscale/swscale.h"
};
#else
//Linux...
#ifdef __cplusplus
extern "C" {
#endif
#include <libavutil/opt.h>
#include <libavcodec/avcodec.h>
#include <libavutil/channel_layout.h>
#include <libavutil/common.h>
#include <libavutil/imgutils.h>
#include <libavutil/mathematics.h>
#include <libavutil/samplefmt.h>

#include <libavformat/avformat.h>
#include <libavcodec/avcodec.h>
#include <libavutil/imgutils.h>
#include <libswscale/swscale.h>
#ifdef __cplusplus
};
#endif
#endif

#include <string>


namespace streamer
{


class Scaler
{
public:
    SwsContext *ctx;

    Scaler()
    {
        ctx = nullptr;
    }

    ~Scaler()
    {
        if(ctx) {
            sws_freeContext(ctx);
        }
    }

    int init(AVCodecContext *codec_ctx, int src_width, int src_height, int dst_width, int dst_height, int flags)
    {
        ctx = sws_getContext(src_width, src_height, AV_PIX_FMT_BGR24, dst_width, dst_height,
                             codec_ctx->pix_fmt, flags, nullptr, nullptr, nullptr);
        if(!ctx) {
            fprintf(stderr, "Could not initialize sample scaler!\n");
            return 1;
        }
        return 0;
    }
};



class Picture
{
    static const int align_frame_buffer = 32;
public:

    AVFrame *frame;
    uint8_t *data;

    int init(enum AVPixelFormat pix_fmt, int width, int height)
    {
        frame = nullptr;
        data = nullptr;
        frame = av_frame_alloc();

        int sz =  av_image_get_buffer_size(pix_fmt, width, height, align_frame_buffer);
        int ret = posix_memalign(reinterpret_cast<void**>(&data), align_frame_buffer, sz);

        av_image_fill_arrays(frame->data, frame->linesize, data, pix_fmt, width, height, align_frame_buffer);
        frame->format = pix_fmt;
        frame->width  = width;
        frame->height = height;

        return ret;
    }

    Picture()
    {
        frame = nullptr;
        data = nullptr;
    }


    ~Picture()
    {
        if(data) {
            free(data);
            data = nullptr;
        }

        if(frame) {
            av_frame_free(&frame);
        }
    }
};


struct StreamerConfig
{
    int src_width;
    int src_height;
    int dst_width;
    int dst_height;
    int fps;
    int bitrate;
    int gop_size;
    std::string profile;
    std::string server;

    StreamerConfig()
    {
        dst_width = 0;
        dst_height = 0;
        src_width = 0;
        src_height = 0;
        fps = 0;
        bitrate = 0;
        gop_size = 12;
    }

    StreamerConfig(int source_width, int source_height, int stream_width, int stream_height, int stream_fps, int stream_bitrate, int stream_gop_size,
                   const std::string &stream_profile,
                   const std::string &stream_server)
    {
        src_width = source_width;
        src_height = source_height;
        dst_width = stream_width;
        dst_height = stream_height;
        fps = stream_fps;
        bitrate = stream_bitrate;
        gop_size = stream_gop_size;
        profile = stream_profile;
        server = stream_server;
    }
};


class Streamer
{
    bool network_init_ok;
    bool rtmp_server_conn;
    bool init_ok;

    AVFormatContext *format_ctx;
    AVCodec *out_codec;
    AVStream *out_stream;
    AVCodecContext *out_codec_ctx;

    Scaler scaler;
    Picture picture;

    void cleanup();
    bool can_stream()
    {
        return network_init_ok && rtmp_server_conn && init_ok;
    }

public:
    double inv_stream_timebase;
    StreamerConfig config;
    Streamer();
    ~Streamer();
    void enable_av_debug_log();
    int init(const StreamerConfig &streamer_config);
    void stream_frame(const uint8_t *data);
    void stream_frame(const uint8_t *data, int64_t frame_duration);

};

} // namespace streamer
#endif
