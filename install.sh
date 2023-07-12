#!/bin/bash

echo "1: Update python setuptools"
sudo pip3 install --upgrade setuptools
echo "2: Install raspi-blinka"
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py
echo "3: Install libraries for sensors"
pip3 install adafruit-circuitpython-lis3dh
pip3 install adafruit-circuitpython-mcp9808
pip3 install asyncio websockets
cd ./modules
git clone https://github.com/wujekbrezniew/python-apds9960
cp -r python-apds9960/apds9960 apds9960
sudo rm -r python-apds9960
sudo reboot
