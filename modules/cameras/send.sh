#!/bin/bash
sftp -i ~/.ssh/img -P 8022 img@golfserver:/images <<< $'put '$1
