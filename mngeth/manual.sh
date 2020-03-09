#geth --datadir $DDR1 --password <(echo -n 1234) account new
#geth --datadir $DDR2 --password <(echo -n 1234) account new
#geth --datadir $DDR3 --password <(echo -n 1234) account new

#geth --datadir=$DDR1 --networkid 714715 --nat extip:172.16.87.133 --netrestrict 172.16.87.0/24 --port 30303 console
#geth --datadir=$DDR2 --networkid 714715 --nat extip:172.16.87.133 --netrestrict 172.16.87.0/24 --port 30304 console
#geth --datadir=$DDR3 --networkid 714715 --nat extip:172.16.87.133 --netrestrict 172.16.87.0/24 --port 30305 console

geth --datadir=$DDR1 --networkid 714715 --nat extip:172.16.87.135 --netrestrict 172.16.87.0/24 --port 30303

#geth attach $DDR1/geth.ipc --exec admin.nodeInfo.enr | tr -d '"' >~/boot.key
#export BT=$(cat ~/boot.key) >>~/.bashrc
#geth --datadir $DDR2 --networkid 714715 --port 30304 --bootnodes $BT

ENODE_ADDRESS="enode://$(bootnode -nodekey $DDR1/geth/nodekey -writeaddress)@172.16.87.135:30303"
ENODE_ADDRESS="enode://$(bootnode -nodekey $DDR1/geth/nodekey -writeaddress)@10.0.0.1:30303"
geth --datadir $DDR2 --networkid 714715 --port 30304 --bootnodes $ENODE_ADDRESS
# 3rd
geth attach $DDR2/geth.ipc --exec admin.peers # check the 2nd node joins
geth --datadir $DDR3 --networkid 714715 --port 30307 --mine --minerthreads=4 --etherbase=0x0213af577d12cf11a5baf5a869e0b1305684ca0a

#geth --datadir=$DDR3 --networkid 714715 --nat extip:10.0.0.1 --netrestrict 10.0.0.0/24 --port 30305 console
geth attach $DDR3/geth.ipc --exec 'web3.fromWei(eth.getBalance(eth.coinbase), "ether")'
killall geth


h2 ENODE_ADDRESS="enode://$(bootnode -nodekey $DDR1/geth/nodekey -writeaddress)@10.0.0.1:30303"
h2 geth --datadir $DDR2 --networkid 714715 --port 30304 --bootnodes $ENODE_ADDRESS
