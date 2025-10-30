# Cultivation sensors  
Code for all cultivation sensors that are used in the experiment.

## Requirements

Any SBC with 2 USBs and 2 I2C interfaces. Install script covers Raspbian compatible devices and Armbian on sun50i-h616 SoC/dt

## Install

Run `./install.sh IP_ADDR P_HOSTNAME` where IP_ADDR is the address of the main server (with the MongoDB database and clinostat_images Docker container) and P_HOSTNAME is the parent hostname (hostname of the clinostat controller, e.g., if your controller hostname is clinostat, then you use "clinostat")

Script covers everything and can detect if your device is running Raspbian or Armbian with sun50i-h616. In case of other devices, you will be asked if you want to continue. You will need to enable two I2C devices later.

## Configure

In config.py, you can configure I2C addresses to which sensors are connected. `to_kill_at_exception` is a switch if you want to stop execution of all threads when an exception occurs in any thread. `False` is disabled.

## Libraries

Those libraries are hard-linked.

`./modules/sensors/ADS1x15` is forked from: https://github.com/chandrawi/ADS1x15-ADC MIT Licensed

`./modules/sensors/apds9960` is forked from https://github.com/liske/python-apds9960 GPL-3.0 Licensed

In both cases, new device IDs were added.

## Misc
In the misc folder, you will find three systemd services. The most important one is `sensors.service`, which you can install to automatically run software at startup. Put it into `/etc/systemd/system/` dir and then enable it with `sudo systemctl enable sensors.service`. To start, run `sudo systemctl start controller.service`.
