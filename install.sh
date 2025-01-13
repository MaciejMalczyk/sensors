#!/bin/bash

STEP=0
RPI=0
BL='\033[1;34m'
NC='\033[0m'

echo -e "${BL} $STEP: Checking connection to server ${NC}"

if ping -c 1 clinostate.server &> /dev/null ; then
    echo -e "Continue..."
else
    echo -e "No connection to clinostate.server. Setup VPN and add address to /etc/hosts"
    exit 0
fi

if command -v raspi-config >/dev/null 2>&1
then
    echo -e "${BL}Raspberry Pi device detected.${NC}"
    RPI=1
else
    echo -e "${BL}Other device detected.${NC}"
fi

if [ $RPI -eq 1 ]
then
    ((STEP++)); echo -e "${BL} $STEP: Enralge swap to 2G ${NC}"
    sudo dphys-swapfile swapoff
    sudo cp ./misc/dphys-swapfile /etc
    sudo dphys-swapfile setup
    sudo dphys-swapfile swapon
fi

((STEP++)); echo -e "${BL} $STEP: Install pip3 and packages ${NC}"
sudo apt update && sudo apt install -y python3-pip python3-opencv python3-fabric python3-smbus python3-systemd v4l-utils i2c-tools avahi-daemon ntp

((STEP++)); echo -e "${BL} $STEP: Update python setuptools ${NC}"
sudo pip3 install --upgrade setuptools --break-system-packages

((STEP++)); echo -e "${BL} $STEP: Install libraries for sensors ${NC}"
pip3 install asyncio websockets ADS1x15-ADC smbus2 pymongo websockets --break-system-packages
cd ./modules || exit 1
git clone https://github.com/wujekbrezniew/python-apds9960
cp -r python-apds9960/apds9960 apds9960
sudo rm -r python-apds9960
cd .. || exit 1

((STEP++)); echo -e "${BL} $STEP: Generate ssh keys ${NC}"
echo -e "/home/$USER/.ssh/img" | ssh-keygen -q -N ""
ssh-copy-id -i ~/.ssh/img -p 8022 img@clinostate.server

if [ $RPI -eq 1 ]
then
    ((STEP++)); echo -e "${BL} $STEP: Setup i2c-0 ${NC}"
    sudo su -c "echo -e dtparam=i2c_vc=on >> /boot/firmware/config.txt"
    sudo raspi-config nonint do_i2c 0

    ((STEP++)); echo -e "${BL} $STEP: Disable wifi power saving ${NC}"
    sudo cp ./misc/rc.local /etc/
fi

((STEP++)); echo -e "${BL} $STEP: Install sensors service ${NC}"
sudo cp ./misc/sensors.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sensors.service

((STEP++)); echo -e "${BL} $STEP: Add user to video group ${NC}"
sudo usermod -a -G video "$USER"

((STEP++)); echo -e "${BL} $STEP: Reboot: 3s ${NC}"
sleep 3s
sudo reboot
