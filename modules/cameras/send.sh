#!/bin/bash
sftp -i ~/.ssh/img -P 8022 img@golfserver.local:/images <<< $'put '$1
