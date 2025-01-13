#!/bin/bash

while true
do
    sleep 600s
    if ! ping -c 1 1.1.1.1 &> /dev/null
    then
        reboot
    fi
done
