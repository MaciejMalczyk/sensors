#!/bin/bash

echo "0: Checking connection to server"

if ping -c 1 golfserver &> /dev/null ; then
    echo "Continue..."
else
    echo "No connection to golfserver. Setup VPN and add address to /etc/hosts"
    exit 0
fi

echo "1: Enralge swap to 2G"
sudo dphys-swapfile swapoff
sudo cp ./misc/dphys-swapfile /etc
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
echo "2: Install pip3 and packages"
sudo apt update && sudo apt install -y python3-pip python3-opencv python3-fabric
echo "3: Update python setuptools"
sudo pip3 install --upgrade setuptools --break-system-packages
echo "4: Install raspi-blinka"
sudo pip3 install --upgrade adafruit-python-shell --break-system-packages
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py
echo "5: Install libraries for sensors"
pip3 install adafruit-circuitpython-lis3dh --break-system-packages
pip3 install adafruit-circuitpython-mcp9808 --break-system-packages
pip3 install asyncio websockets ADS1x15-ADC smbus pymongo websockets --break-system-packages
cd ./modules
git clone https://github.com/wujekbrezniew/python-apds9960
cp -r python-apds9960/apds9960 apds9960
sudo rm -r python-apds9960
cd ..
echo "6: Generate ssh keys"
echo "/home/$USER/.ssh/img" | ssh-keygen
ssh-copy-id -i ~/.ssh/img -p 8022 img@golfserver
echo "7: Setup i2c-0"
sudo su -c "echo dtparam=i2c_vc=on >> /boot/firmware/config.txt"
echo "8: Disable wifi power saving"
sudo cp ./misc/rc.local /etc/
echo "9: Install sensors service"
sudo cp ./misc/sensors.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sensors.service
echo "10: Reboot"
sudo reboot
