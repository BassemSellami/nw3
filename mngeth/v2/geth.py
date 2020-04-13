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

geth_bin_file = 'geth'

bootnode_port = 30303
network_id = 714715
miner_thread = 1
node_1_miner_base = "0x67e37abe6fb7bb2b0d61b9c6f53c71623ae65551"
node_2_miner_base = "0x2dec65f7f6fecef9088afed7ab41ad0f1173ddb4"
node_3_miner_base = "0x0213af577d12cf11a5baf5a869e0b1305684ca0a"
node_4_miner_base = "0x7d8466475a66c4363da52494af4a3c20298f5f73"

gen_enode = (f"ENODE_ADDRESS=\"enode://$(bootnode -nodekey $DDR1/geth/nodekey -writeaddress)"
             f"@{node_1}:{bootnode_port}\"")

node_1_start = (
    f"nohup {geth_bin_file} --datadir=$DDR1 --networkid {network_id} --port {bootnode_port} "
    f"--nat extip:{node_1} --netrestrict 10.0.0.0/24 "
    f"--mine --minerthreads={miner_thread} --etherbase={node_1_miner_base} "
    f"> ~/nw3/mngeth/data/nohup-{node_1}.out &")
node_2_start = (
    f"nohup {geth_bin_file} --datadir $DDR2 --networkid {network_id} --port {bootnode_port + 1} "
    f"--nat extip:{node_2} --netrestrict 10.0.0.0/24 "
    f"--bootnodes $ENODE_ADDRESS "
    f"--mine --minerthreads={miner_thread} --etherbase={node_2_miner_base} "
    f"> ~/nw3/mngeth/data/nohup-{node_2}.out &")
node_3_start = (
    f"nohup {geth_bin_file} --datadir $DDR3 --networkid {network_id} --port {bootnode_port + 2} "
    f"--nat extip:{node_3} --netrestrict 10.0.0.0/24 "
    f"--bootnodes $ENODE_ADDRESS "
    f"--mine --minerthreads={miner_thread} --etherbase={node_3_miner_base} "
    f"> ~/nw3/mngeth/data/nohup-{node_3}.out &")
node_4_start = (
    f"nohup {geth_bin_file} --datadir $DDR4 --networkid {network_id} --port {bootnode_port + 3} "
    f"--nat extip:{node_4} --netrestrict 10.0.0.0/24 "
    f"--bootnodes $ENODE_ADDRESS "
    f"--mine --minerthreads={miner_thread} --etherbase={node_4_miner_base} "
    f"> ~/nw3/mngeth/data/nohup-{node_4}.out &")

node_2_check_join = f"{geth_bin_file} attach $DDR2/geth.ipc --exec admin.peers"
node_3_check_join = f"{geth_bin_file} attach $DDR3/geth.ipc --exec admin.peers"
node_4_check_join = f"{geth_bin_file} attach $DDR4/geth.ipc --exec admin.peers"

node_1_check_blocks = (f"{geth_bin_file} attach $DDR1/geth.ipc "
                       f"--exec 'eth.getBlock(\"latest\")'")
node_2_check_blocks = (f"{geth_bin_file} attach $DDR2/geth.ipc "
                       f"--exec 'eth.getBlock(\"latest\")'")
node_3_check_mine = (f"{geth_bin_file} attach $DDR3/geth.ipc "
                     f"--exec 'web3.fromWei(eth.getBalance(eth.coinbase), \"ether\")'")
node_4_check_mine = (f"{geth_bin_file} attach $DDR4/geth.ipc "
                     f"--exec 'web3.fromWei(eth.getBalance(eth.coinbase), \"ether\")'")
node_1_check_blocks_alt = (f"{geth_bin_file} attach $DDR1/geth.ipc "
                           f"--exec 'eth.getBlock(\"latest\")' > ~/nw3/mngeth/data/nohup-node_1_block.out")


def read_get_block(file="./data/nohup-node_1_block.out"):
    with open(file) as f:
        for line in f.readlines():
            if "number" in line:
                # print(line)
                num = line.strip().split(":")[-1][:-1]
                return int(num)
        raise Exception("no 'number' field found error")
        # data = json.load(f)
        # print(data["difficulty"], data["number"])

# change gas limit
# change topology
