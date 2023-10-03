#!/bin/bash
sftp -i ~/.ssh/img -P 8022 img@192.168.88.247:/images <<< $'put '$1
