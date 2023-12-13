#!/bin/bash

echo "0: Checking connection to server"

if ping -c 1 192.168.100.1 &> /dev/null ; then
    echo "Continue..."
else
    echo "No connection to server. Install zerotier and connect to proper network."
    exit 0
fi

echo "1: Install pip3"
sudo apt update && sudo apt install -y python3-pip python3-opencv git
echo "2: Update python setuptools"
sudo pip3 install --upgrade setuptools --break-system-packages
echo "3: Install raspi-blinka"
sudo pip3 install --upgrade adafruit-python-shell --break-system-packages
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py
echo "4: Install libraries for sensors"
pip3 install adafruit-circuitpython-lis3dh --break-system-packages
pip3 install adafruit-circuitpython-mcp9808 --break-system-packages
pip3 install asyncio websockets ADS1x15-ADC smbus pymongo websockets --break-system-packages
cd ./modules
git clone https://github.com/wujekbrezniew/python-apds9960
cp -r python-apds9960/apds9960 apds9960
sudo rm -r python-apds9960
cd ..
echo "5: Generate ssh keys"
sudo sed -i "2i192.168.100.1    golfserver" /etc/hosts
echo "/home/$USER/.ssh/img" | ssh-keygen
ssh-copy-id -i ~/.ssh/img -p 8022 img@golfserver
echo "6: Setup i2c-0"
sudo su -c "echo dtparam=i2c_vc=on >> /boot/config.txt"
echo "7: Disable wifi power saving"
sudo cp ./misc/rc.local /etc/
echo "8: Install sensors service"
sudo cp ./misc/sensors.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sensors.service
echo "9: Chmod files"
chmod +x ./modules/cameras/send.sh
sudo reboot
