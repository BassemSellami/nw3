import json

# node 1: full node (bootnode)
# node 2: full node
# node 3: miner 1
# node 4: miner 2
node_1 = "10.0.0.1"
node_2 = "10.0.0.2"
node_3 = "10.0.0.3"
node_4 = "10.0.0.4"
node_5 = "10.0.0.5"
node_6 = "10.0.0.6"

bootnode_port = 30303
network_id = 714715
node_3_miner_base = "0x0213af577d12cf11a5baf5a869e0b1305684ca0a"
node_4_miner_base = "0x7d8466475a66c4363da52494af4a3c20298f5f73"

gen_enode = (f"ENODE_ADDRESS=\"enode://$(bootnode -nodekey $DDR1/geth/nodekey -writeaddress)"
             f"@{node_1}:{bootnode_port}\"")

node_1_start = (
    f"nohup ~/go-ethereum/build/bin/geth --datadir=$DDR1 --networkid {network_id} --port {bootnode_port} "
    f"--nat extip:{node_1} --netrestrict 10.0.0.0/24 "
    f"> nohup-{node_1}.out &")

node_2_start = (
    f"nohup ~/go-ethereum/build/bin/geth --datadir $DDR2 --networkid {network_id} --port {bootnode_port + 1} "
    f"--nat extip:{node_2} --netrestrict 10.0.0.0/24 "
    f"--bootnodes $ENODE_ADDRESS "
    f"> nohup-{node_2}.out &")
node_3_start = (
    f"nohup ~/go-ethereum/build/bin/geth --datadir $DDR3 --networkid {network_id} --port {bootnode_port + 2} "
    f"--nat extip:{node_3} --netrestrict 10.0.0.0/24 "
    f"--bootnodes $ENODE_ADDRESS --mine --minerthreads=1 --etherbase={node_3_miner_base} "
    f"> nohup-{node_3}.out &")
node_4_start = (
    f"nohup ~/go-ethereum/build/bin/geth --datadir $DDR4 --networkid {network_id} --port {bootnode_port + 3} "
    f"--nat extip:{node_4} --netrestrict 10.0.0.0/24 "
    f"--bootnodes $ENODE_ADDRESS --mine --minerthreads=2 --etherbase={node_4_miner_base} "
    f"> nohup-{node_4}.out &")

node_2_check_join = "~/go-ethereum/build/bin/geth attach $DDR2/geth.ipc --exec admin.peers"
node_3_check_join = "~/go-ethereum/build/bin/geth attach $DDR3/geth.ipc --exec admin.peers"
node_4_check_join = "~/go-ethereum/build/bin/geth attach $DDR4/geth.ipc --exec admin.peers"

node_1_check_blocks = "~/go-ethereum/build/bin/geth attach $DDR1/geth.ipc --exec 'eth.getBlock(\"latest\")'"
node_2_check_blocks = "~/go-ethereum/build/bin/geth attach $DDR2/geth.ipc --exec 'eth.getBlock(\"latest\")'"
node_3_check_mine = "~/go-ethereum/build/bin/geth attach $DDR3/geth.ipc --exec 'web3.fromWei(eth.getBalance(eth.coinbase), \"ether\")'"
node_4_check_mine = "~/go-ethereum/build/bin/geth attach $DDR4/geth.ipc --exec 'web3.fromWei(eth.getBalance(eth.coinbase), \"ether\")'"

node_1_check_blocks_alt = "~/go-ethereum/build/bin/geth attach $DDR1/geth.ipc --exec 'eth.getBlock(\"latest\")' > nohup_node_1_block.out"


def read_get_block(file="/root/nohup_node_1_block.out"):
    with open(file) as f:
        for line in f.readlines():
            if "number" in line:
                # print(line)
                num = line.strip().split(":")[-1][:-1]
                return int(num)
        raise Exception("no 'number' field found error")
        # data = json.load(f)
        # print(data["difficulty"], data["number"])

# 改blocksize
# 改topology
