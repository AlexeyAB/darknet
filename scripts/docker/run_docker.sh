#!/bin/bash

# Help and arguments to STOUT
function print_help (){
    echo "Script for running ProgNets through docker"
    echo "Usage ./run_docker.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "-p, --pull        Pull the image before running."
    echo "-v, --volume_dir  Directory for volume mount."
    echo "--no-nvidia       Run the container without nvidia."
    echo "--nvidia-docker2  Run the container with nvidia-docker2"
}

# Default arguments.

# Build docker container before run. Set true for this
# script to build the docker files before the docker run
# command.
do_pull="false"

# Use nvidia-docker for GPU acceleration. Set false to
# run with standard docker run.
use_nvidia="true"
use_nvidia_docker2="false"

# Volume directory for the mount between the container
# and your local box. Defauls to /home/user. Mac users
# may need to set this argument for their system.
volume_dir="/home/$(whoami)"

# Read command line args.
while test 5 -gt 0; do
    case "$1" in
        -h|--help)
            print_help
            exit 0
            ;;
        -p|--pull)
            do_pull="true"
            shift
            ;;
        -v|--volume_dir)
            volume_dir=`echo $2`
            shift
            shift
            ;;
        --no-nvidia)
            use_nvidia="false"
            shift
            ;;
        --nvidia-docker2)
            use_nvidia_docker2="true"
            shift
            ;;
        *)
        break
        ;;
    esac
done


# Main. Runs docker image according to above specified arguments.
function main () {

    if [[ "$do_pull" == "true" ]]; then
        # Pull image.
        docker pull alemelis/darknet:latest
    fi

    # Switch docker executables based on use_nvidia flag.
    if [[ "$use_nvidia" == "true" ]]; then
        # Nvidia.
        if [[ "$use_nvidia_docker2" == "true" ]]; then
            docker run --gpus all -u $(id -u):$(id -g) \
                -v /home/$(whoami):/home/$(whoami) \
                -w /app/darknet/ --rm -it \
                --entrypoint=/bin/bash alemelis/darknet
        else
            nvidia-docker run -u $(id -u):$(id -g) \
                -v $volume_dir:/home/$(whoami) \
                -w /app/darknet/ --rm -it \
                --entrypoint=/bin/bash --runtime=nvidia alemelis/darknet
        fi
    else
        # Non-nvidia
        docker run -u $(id -u):$(id -g) \
            -v $volume_dir:/home/$(whoami) \
            -w /app/darknet/ --rm -it \
            --entrypoint=/bin/bash alemelis/darknet
    fi
}

# Entry point.
main

