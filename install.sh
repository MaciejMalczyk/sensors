#!/bin/bash

if [ "$1" = "-h" ] ; then
    echo "Install script for cultivation"
    echo "\$1 - ip address of main server"
    echo "\$2 - parent device hostname"
    exit 0
fi

SCRIPT_SERVER_IP=$1
SCRIPT_DEVICE_HOSTNAME=$2
STEP=0
DEVICE=0
BL='\033[1;34m'
NC='\033[0m'

if command -v raspi-config > /dev/null 2>&1
then
    echo -e "${BL}Raspberry Pi device detected.${NC}"
    DEVICE=1
elif grep 'sun50i-h616' /boot/armbianEnv.txt > /dev/null
then
    echo -e "${BL}Armbian device detected.${NC}"
    DEVICE=2
else
    echo -e "${BL}Other device detected. Do at your own risk.${NC}"
    read -rsn1 -p "${BL}Continue (y/any) ??${NC}" ANSWER;
    if [ "$ANSWER" != "y" ] ; then
        exit 0
    fi
fi

# Main script

echo -e "${BL} $STEP: Setting hostnames ${NC}"
if [ "$SCRIPT_SERVER_IP" ] && [ "$SCRIPT_DEVICE_HOSTNAME" ] ; then
    echo "$SCRIPT_SERVER_IP clinostate.server" | sudo tee -a /etc/hosts
    sudo hostnamectl set-hostname "$SCRIPT_DEVICE_HOSTNAME-cultivation"
else
    echo "No proper server ip and hostname given. Use -h to check options."
    exit 0
fi

((STEP++)); echo -e "${BL} $STEP: Checking server ${NC}"
if ping -c 1 "clinostate.server" &> /dev/null ; then
    echo -e "Continue..."
else
    echo -e "No connection to clinostate.server ($SCRIPT_SERVER_IP). Check network settings and /etc/hosts file."
    exit 0
fi

if [ "$DEVICE" -eq 1 ]
then
    ((STEP++)); echo -e "${BL} $STEP: Enralge swap to 2G ${NC}"
    sudo dphys-swapfile swapoff
    sudo cp ./misc/dphys-swapfile /etc
    sudo dphys-swapfile setup
    sudo dphys-swapfile swapon
fi

((STEP++)); echo -e "${BL} $STEP: Install pip3 and packages ${NC}"
sudo apt update && sudo apt install -y python3-pip python3-opencv python3-fabric v4l-utils

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

if [ "$DEVICE" -eq 1 ]
then
    ((STEP++)); echo -e "${BL} $STEP: Setup i2c-0 ${NC}"
    sudo su -c "echo -e dtparam=i2c_vc=on >> /boot/firmware/config.txt"
    sudo raspi-config nonint do_i2c 0

    ((STEP++)); echo -e "${BL} $STEP: Disable wifi power saving ${NC}"
    sudo cp ./misc/rc.local /etc/
fi

if [ "$DEVICE" -eq 2 ]
then
    ((STEP++)); echo -e "${BL} $STEP: Setup sun50i-h616 i2c overlays ${NC}"
    sed 's/overlays=.*/overlays=i2c1-pi i2c2-pi/' /boot/armbianEnv.txt
fi

((STEP++)); echo -e "${BL} $STEP: Install sensors service ${NC}"
sudo cp ./misc/sensors.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sensors.service

((STEP++)); echo -e "${BL} $STEP: Reboot: 3s ${NC}"
sleep 3s
sudo reboot
