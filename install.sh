#!/bin/bash

STEP=0

echo "$STEP: Checking connection to server"

if ping -c 1 clinostate.server &> /dev/null ; then
    echo "Continue..."
else
    echo "No connection to clinostate.server. Setup VPN and add address to /etc/hosts"
    exit 0
fi

((STEP++)); echo "$STEP: Enralge swap to 2G"
sudo dphys-swapfile swapoff
sudo cp ./misc/dphys-swapfile /etc
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
((STEP++)); echo "$STEP: Install pip3 and packages"
sudo apt update && sudo apt install -y python3-pip python3-opencv python3-fabric v4l-utils
((STEP++)); echo "$STEP: Update python setuptools"
sudo pip3 install --upgrade setuptools --break-system-packages
((STEP++)); echo "$STEP: Install libraries for sensors"
pip3 install asyncio websockets ADS1x15-ADC smbus pymongo websockets --break-system-packages
cd ./modules || exit 1
git clone https://github.com/wujekbrezniew/python-apds9960
cp -r python-apds9960/apds9960 apds9960
sudo rm -r python-apds9960
cd .. || exit 1
((STEP++)); echo "$STEP: Generate ssh keys"
echo "/home/$USER/.ssh/img" | ssh-keygen
ssh-copy-id -i ~/.ssh/img -p 8022 img@clinostate.server
((STEP++)); echo "$STEP: Setup i2c-0"
sudo su -c "echo dtparam=i2c_vc=on >> /boot/firmware/config.txt"
sudo raspi-config nonint do_i2c 0
((STEP++)); echo "$STEP: Disable wifi power saving"
sudo cp ./misc/rc.local /etc/
((STEP++)); echo "$STEP: Install sensors service"
sudo cp ./misc/sensors.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sensors.service
((STEP++)); echo "$STEP: Reboot: 3s"
sleep 3s
sudo reboot
