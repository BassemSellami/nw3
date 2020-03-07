#!/usr/bin/env bash
# for ubuntu 18.04

#sudo apt-get update -y
#sudo apt-get install -y \
#    apt-transport-https \
#    ca-certificates \
#    curl \
#    gnupg-agent \
#    software-properties-common
#curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
#sudo apt-key fingerprint 0EBFCD88
#sudo add-apt-repository \
#   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
#   $(lsb_release -cs) \
#   stable"
#sudo apt-get update -y
#sudo apt-get install -y docker-ce docker-ce-cli containerd.io
#sudo docker run hello-world
#
#
#apt update
#apt install -y iputils-ping
#apt install -y iproute2
#ip addr show

sudo apt update
sudo apt-get install ansible git aptitude
git clone https://github.com/containernet/containernet.git
cd containernet/ansible
sudo ansible-playbook -i "localhost," -c local install.yml
cd ..