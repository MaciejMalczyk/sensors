#!/bin/bash

echo "1: Install pip3"
sudo apt update && sudo apt install -y python3-pip python3-opencv
echo "2: Update python setuptools"
sudo pip3 install --upgrade setuptools
echo "3: Install raspi-blinka"
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py
echo "4: Install libraries for sensors"
pip3 install adafruit-circuitpython-lis3dh
pip3 install adafruit-circuitpython-mcp9808
pip3 install asyncio websockets ADS1x15-ADC smbus pymongo websockets
cd ./modules
git clone https://github.com/wujekbrezniew/python-apds9960
cp -r python-apds9960/apds9960 apds9960
sudo rm -r python-apds9960
echo "5: Generate ssh keys"
echo "/home/$USER/.ssh/img" | ssh-keygen
ssh-copy-id -i ~/.ssh/img -p 8022 img@192.168.1.102
echo "6: Setup i2c-0"
sudo su -c "echo dtparam=i2c_vc=on >> /boot/config.txt"
sudo reboot
