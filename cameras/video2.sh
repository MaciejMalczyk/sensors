#!/bin/bash

image="video2_$(date +%Y%m%d_%H%M%S).jpg"

fswebcam -d /dev/video2 -r 2592x1944 --no-banner $image

sftp -i ~/.ssh/id_rsa -P 8022 img@helmholtz.polsl.pl:/images <<< $'put '$image
