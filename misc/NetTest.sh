#!/bin/bash

while true
do
    if ! ping -c 1 1.1.1.1 &> /dev/null
    then
        reboot
    fi
    sleep 60s
done
