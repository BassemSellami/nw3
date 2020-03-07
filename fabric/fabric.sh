# ubuntu-18.04.3-live-server-amd64.iso

# https://www.cyberciti.biz/faq/change-root-password-ubuntu-linux/
# https://askubuntu.com/questions/511833/cant-ssh-in-as-root
# ssh root@172.16.87.136

sudo apt update
sudo apt -y upgrade
sudo apt install -y build-essential linux-headers-$(uname -r)
sudo apt install -y git zip python3-pip

# install docker
sudo apt-get update
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo docker run hello-world
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# install go
cd
wget -q https://dl.google.com/go/go1.14.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.14.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> /etc/profile
echo 'export GOPATH=/usr/local/go' >> /etc/profile

# nodejs
cd
wget -q https://nodejs.org/dist/v12.16.1/node-v12.16.1-linux-x64.tar.xz
tar -C /usr/local -xf node-v12.16.1-linux-x64.tar.xz
echo 'export PATH=$PATH:/usr/local/node-v12.16.1-linux-x64/bin' >> /etc/profile

cd
rm go1.14.linux-amd64.tar.gz node-v12.16.1-linux-x64.tar.xz

git clone https://github.com/hyperledger/fabric-samples.git
cd fabric-samples
git checkout release-1.4
curl -sSL http://bit.ly/2ysbOFE | bash -s -- 1.4.6 1.4.6 0.4.18
echo 'export PATH=$PATH:~/fabric-samples/bin' >>~/.bashrc

