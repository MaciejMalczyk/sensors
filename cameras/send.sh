#!/bin/bash
sftp -i ~/.ssh/img -P 8022 img@helmholtz.polsl.pl:/images <<< $'put '$1
