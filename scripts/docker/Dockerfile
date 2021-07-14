FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

ARG DEBIAN_FRONTEND=noninteractive

MAINTAINER Alessandro Melis <alessandro_melis@rocketmail.com>

WORKDIR /app

RUN apt update 
RUN apt install -y \
	pkg-config git build-essential libopencv-dev

# build darknet
RUN git clone https://github.com/AlexeyAB/darknet.git
WORKDIR darknet
RUN make OPENCV=1 GPU=1 AVX=1 OPENMP=1 CUDNN=1 OPENMP=1 CUDNN_HALF=1 -j $(nproc)
RUN chmod +x darknet

COPY bash.bashrc /etc/

ENTRYPOINT ["/app/darknet/darknet"]
