sudo apt update
sudo apt -y upgrade
sudo apt install -y build-essential linux-headers-$(uname -r)
sudo apt install -y git zip python3-pip

sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install -y ethereum

git clone https://github.com/haochenpan/nw3

cd
mkdir -p ethData1/keystore
mkdir -p ethData2/keystore
mkdir -p ethData3/keystore
echo export DDR1=~/ethData1 >> ~/.bashrc
echo export DDR2=~/ethData2 >> ~/.bashrc
echo export DDR3=~/ethData3 >> ~/.bashrc
source  ~/.bashrc


geth --datadir $DDR1 --password <(echo -n 1234) account new
geth --datadir $DDR2 --password <(echo -n 1234) account new
geth --datadir $DDR3 --password <(echo -n 1234) account new


# replace keys, save the following as genesis.json


geth init --datadir $DDR1 genesis.json
geth init --datadir $DDR2 genesis.json
geth init --datadir $DDR3 genesis.json

geth --datadir=$DDR1 --networkid 714714 --nat extip:172.16.87.133 --netrestrict 172.16.87.0/24 console
geth --datadir=$DDR2 --networkid 714714 --nat extip:172.16.87.133 --netrestrict 172.16.87.0/24 --port 30307 console
geth --datadir=$DDR3 --networkid 714714 --nat extip:172.16.87.133 --netrestrict 172.16.87.0/24 --port 30308 console

# 2nd
geth attach $DDR1/geth.ipc --exec admin.nodeInfo.enr | tr -d '"' > ~/boot.key
echo export BT=$(cat ~/boot.key) >> ~/.bashrc
source ~/.bashrc
geth --datadir $DDR2 --networkid 714714 --port 30304 --bootnodes $BT

# 3rd
geth attach $DDR2/geth.ipc --exec admin.peers
geth --datadir $DDR3 --networkid 714714 --port 30307 --mine --minerthreads=1 --etherbase=0x0213AF577D12cF11a5baF5a869e0B1305684cA0A
geth --datadir $DDR2 --networkid 714714 --port 30307 --mine --minerthreads=3 --etherbase=0x2dEC65F7F6FECef9088Afed7AB41Ad0F1173DDb4


# mine
geth --mine --minerthreads=1 --datadir $DDR --networkid 714714