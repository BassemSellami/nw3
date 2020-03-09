sudo apt update
sudo apt -y upgrade
sudo apt install -y build-essential linux-headers-$(uname -r)
sudo apt install -y git zip python3-pip

sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install -y ethereum

cd
mkdir mininet
cd mininet
git clone git://github.com/mininet/mininet
cd mininet
git checkout -b 2.2.2
cd ..
mininet/util/install.sh -a
sudo mn --test pingall

cd
mkdir -p ethData1/keystore
mkdir -p ethData2/keystore
mkdir -p ethData3/keystore
cp ~/nw3/mngeth/UTC--2020-03-07T23-25-18.301273092Z--67e37abe6fb7bb2b0d61b9c6f53c71623ae65551 ethData1/keystore
cp ~/nw3/mngeth/UTC--2020-03-07T23-27-12.170957487Z--2dec65f7f6fecef9088afed7ab41ad0f1173ddb4 ethData2/keystore
cp ~/nw3/mngeth/UTC--2020-03-07T23-27-53.050585459Z--0213af577d12cf11a5baf5a869e0b1305684ca0a ethData3/keystore
echo export DDR1=~/ethData1 >>~/.bashrc
echo export DDR2=~/ethData2 >>~/.bashrc
echo export DDR3=~/ethData3 >>~/.bashrc
source ~/.bashrc
