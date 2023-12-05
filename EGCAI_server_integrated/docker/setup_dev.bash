#!/bin/bash

endo_docker() {
  xhost +local:docker;
  docker run -it -d \
    --gpus all \
    --name="endo_dev" \
    -p 10002:22 \
    -p 9999:9999 \
    -v /etc/localtime:/etc/localtime:ro \
    -v /dev/input:/dev/input \
    -v "$DATASETS:$HOME/datasets" \
    -v "$Endo_GIT:$HOME/Endo" \
    --shm-size=8G \
    --workdir $HOME/ \
    --env=DISPLAY \
    --env=XDG_RUNTIME_DIR \
    --env=QT_X11_NO_MITSHM=1 \
    --device=/dev/dri:/dev/dri \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v /etc/localtime:/etc/localtime:ro \
    endo:latest
    endo_docker_attach;
}

endo_docker_attach() {
  docker exec -it endo_dev /bin/bash
}

