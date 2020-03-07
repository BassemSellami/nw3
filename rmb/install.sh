#!/usr/bin/env bash
# for ubuntu 18.04

sudo apt update && sudo apt upgrade -y
sudo apt install build-essential linux-headers-$(uname -r) -y
sudo apt install git zip -y
sudo apt install python3-pip -y

cd
mkdir mininet
cd mininet
git clone git://github.com/mininet/mininet
cd mininet
git checkout -b 2.2.2
cd ..
mininet/util/install.sh -a

sudo mn --test pingall


