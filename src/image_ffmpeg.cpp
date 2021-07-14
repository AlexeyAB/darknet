#include "image.h"
#include <opencv2/opencv.hpp>
#include <iostream>
#include "darknet.h"

#include "image_opencv.h"
#include "image_ffmpeg.h"

#ifdef __cplusplus
extern "C" {
#endif

#include "libavcodec/avcodec.h"
#include "libavdevice/avdevice.h"
#include "libavformat/avformat.h"
#include "libavfilter/avfilter.h"
#include "libavutil/avutil.h"
#include "libavutil/time.h"
#include "libswscale/swscale.h"
#include "libavutil/pixdesc.h"

#ifdef __cplusplus
}
#endif

#pragma comment(lib, "avformat.lib")
#pragma comment(lib, "avdevice.lib")
#pragma comment(lib, "avcodec.lib")
#pragma comment(lib, "avutil.lib")
#pragma comment(lib, "avfilter.lib")
#pragma comment(lib, "swscale.lib")
#pragma comment(lib, "swresample.lib")
#pragma comment(lib, "postproc.lib")

using namespace std;
using namespace cv;

image mat_to_image(cv::Mat mat)
{
    int w = mat.cols;
    int h = mat.rows;
    int c = mat.channels();
    image im = make_image(w, h, c);
    unsigned char *data = (unsigned char *)mat.data;
    int step = mat.step;
    for (int y = 0; y < h; ++y) {
        for (int k = 0; k < c; ++k) {
            for (int x = 0; x < w; ++x) {
                //uint8_t val = mat.ptr<uint8_t>(y)[c * x + k];
                //uint8_t val = mat.at<Vec3b>(y, x).val[k];
                //im.data[k*w*h + y*w + x] = val / 255.0f;
                im.data[k*w*h + y*w + x] = data[y*step + x*c + k] / 255.0f;
            }
        }
    }
    return im;
}

#ifdef __cplusplus
extern "C" {
#endif

bool nRestart = false;
AVFormatContext *ifmt_ctx = NULL;
AVStream *pVst;
AVCodecContext *pVideoCodecCtx = NULL;
AVCodec *pVideoCodec = NULL;
IplImage *pRgbImg;
AVFrame *pFrame = av_frame_alloc();
int got_picture;
//uint8_t* buffer_rgb = NULL;
AVFrame         *pFrameRGB = av_frame_alloc();
SwsContext      *img_convert_ctx = NULL;
//cv::Mat Img;
AVDictionary *optionsDict = NULL;
char            errbuf[64];
unsigned int    i;
AVStream        *st = NULL;
AVPacket pkt;
int video_st_index = -1;
int audio_st_index = -1;
int ret;

#ifdef FFMPEG
void close_stream()
{
    if (NULL != ifmt_ctx) {
		avformat_close_input(&ifmt_ctx);
		ifmt_ctx = NULL;
	}
    exit(0);
}

extern "C" void av_pkt_unref()
{
    av_packet_unref(&pkt);
}

extern "C" void open_video_stream(const char *filename)
{
    av_register_all();                                                          // Register all codecs and formats so that they can be used.
    avformat_network_init();                                                    // Initialization of network components
    av_dict_set(&optionsDict, "rtsp_transport", "tcp", 0);                //采用tcp传输	,,如果不设置这个有些rtsp流就会卡着
    av_dict_set(&optionsDict, "stimeout", "2000000", 0);                  //如果没有设置stimeout

    av_init_packet(&pkt);                                                       // initialize packet.
    pkt.data = NULL;
    pkt.size = 0;

    if ((ret = avformat_open_input(&ifmt_ctx, filename, 0, &optionsDict)) < 0) {            // Open the input file for reading.
        printf("Could not open input file '%s' (error '%s')\n", filename, av_make_error_string(errbuf, sizeof(errbuf), ret));
        close_stream();
    }

    if ((ret = avformat_find_stream_info(ifmt_ctx, NULL)) < 0) {                // Get information on the input file (number of streams etc.).
        printf("Could not open find stream info (error '%s')\n", av_make_error_string(errbuf, sizeof(errbuf), ret));
        close_stream();
    }

    for (i = 0; i < ifmt_ctx->nb_streams; i++) {                                // dump information
        av_dump_format(ifmt_ctx, i, filename, 0);
    }

    for (i = 0; i < ifmt_ctx->nb_streams; i++) {                                // find video stream index
        st = ifmt_ctx->streams[i];
        switch (st->codec->codec_type) {
        case AVMEDIA_TYPE_AUDIO: audio_st_index = i; break;
        case AVMEDIA_TYPE_VIDEO: video_st_index = i; break;
        default: break;
        }
    }
    if (-1 == video_st_index) {
        printf("No H.264 video stream in the input file\n");
        close_stream();
    }
}

extern "C" image get_image_from_ffmpeg_stream_resize(mat_cv** in_image, int w, int h, int c)
{
    cv::Mat *mat = NULL;
    image empty_im = make_empty_image(0,0,0);

    //cv::Mat Img;

    do{
        ret = av_read_frame(ifmt_ctx, &pkt);                                // read frames
    }while(ret == AVERROR(EAGAIN) || pkt.stream_index != video_st_index);

    if (ret < 0) {
        printf("Could not read frame ---(error '%s')\n", av_make_error_string(errbuf, sizeof(errbuf), ret));
        close_stream();
    }

    if (pkt.stream_index == video_st_index) {                               // video frame
        printf("Video Packet size = %d\n", pkt.size);
    }
    else if (pkt.stream_index == audio_st_index) {                         // audio frame
        printf("Audio Packet size = %d\n", pkt.size);
    }
    else {
        printf("Unknow Packet size = %d\n", pkt.size);
    }

    //decode stream
    if (!nRestart)
    {
        pVst = ifmt_ctx->streams[video_st_index];
        pVideoCodecCtx = pVst->codec;
        pVideoCodec = avcodec_find_decoder(pVideoCodecCtx->codec_id);
        if (pVideoCodec == NULL)
            return empty_im;
        //pVideoCodecCtx = avcodec_alloc_context3(pVideoCodec);

        if (avcodec_open2(pVideoCodecCtx, pVideoCodec, NULL) < 0)
            return empty_im;
        nRestart = true;
    }

    if (pkt.stream_index == video_st_index)
    {
        fprintf(stdout, "pkt.size=%d,pkt.pts=%lld, pkt.data=0x%x.\n", pkt.size, pkt.pts, (unsigned int)pkt.data);
        int av_result = avcodec_decode_video2(pVideoCodecCtx, pFrame, &got_picture, &pkt);

        if (got_picture)
        {
            fprintf(stdout, "decode one video frame!\n");
        }

        if (av_result < 0)
        {
            fprintf(stderr, "decode failed: inputbuf = 0x%x , input_framesize = %d\n", pkt.data, pkt.size);
            return empty_im;
        }
        if (got_picture)
        {
            int bytes = avpicture_get_size(AV_PIX_FMT_RGB24, pVideoCodecCtx->width, pVideoCodecCtx->height);
            uint8_t *buffer_rgb = (uint8_t *)av_malloc(bytes);
            avpicture_fill((AVPicture *)pFrameRGB, buffer_rgb, AV_PIX_FMT_RGB24, pVideoCodecCtx->width, pVideoCodecCtx->height);

            img_convert_ctx = sws_getContext(pVideoCodecCtx->width, pVideoCodecCtx->height, pVideoCodecCtx->pix_fmt,
                pVideoCodecCtx->width, pVideoCodecCtx->height, AV_PIX_FMT_BGR24, SWS_FAST_BILINEAR, NULL, NULL, NULL);
            if (img_convert_ctx == NULL)
            {

                printf("can't init convert context!\n");
                return empty_im;
            }
            sws_scale(img_convert_ctx, pFrame->data, pFrame->linesize, 0, pVideoCodecCtx->height, pFrameRGB->data, pFrameRGB->linesize);
            pRgbImg = cvCreateImage(cvSize(pVideoCodecCtx->width, pVideoCodecCtx->height), 8, 3);

            memcpy(pRgbImg->imageData, buffer_rgb, pVideoCodecCtx->width * 3 * pVideoCodecCtx->height);
            //image im = ipl_to_image(pRgbImg);

            mat = new cv::Mat();
            *mat = cvarrToMat(pRgbImg);

            //Img = cvarrToMat(pRgbImg);
            cvReleaseImage(&pRgbImg);
            sws_freeContext(img_convert_ctx);
            av_free(buffer_rgb);
        }
    }

    //*(cv::Mat **)in_image = &Img;
    *(cv::Mat **)in_image = mat;

    cv::Mat new_img = cv::Mat(h, w, CV_8UC(c));
    cv::resize(*mat, new_img, new_img.size(), 0, 0, cv::INTER_LINEAR);
    cv::cvtColor(new_img, new_img, cv::COLOR_RGB2BGR);
    image im = mat_to_image(new_img);

    return im;
}


#endif  // FFMPEG

#ifdef __cplusplus
}
#endif
