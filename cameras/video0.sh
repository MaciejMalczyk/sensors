#!/bin/bash

image="video0_$(date +%Y%m%d_%H%M%S).jpg"

fswebcam -d /dev/video0 -r 2592x1944 --no-banner $image

sftp -i ~/.ssh/id_rsa -P 8022 img@helmholtz.polsl.pl:/images <<< $'put '$image
