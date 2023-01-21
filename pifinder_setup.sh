#! /usr/bin/bash
sudo apt -y install git python3-pip
git clone https://github.com/brickbots/PiFinder.git
cd PiFinder
sudo pip install -r requirements.txt
cd python/PiFinder
git clone https://github.com/esa/tetra3.git
echo "dtparam=spi=on" | sudo tee -a /boot/config.txt
echo "dtparam=i2c_arm=on" | sudo tee -a /boot/config.txt
echo "dtparam=i2c1=on" | sudo tee -a /boot/config.txt