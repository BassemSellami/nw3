bootnode_ip = "10.0.0.1"
bootnode_port = 30303
network_id = "714715"
miner_base = "0x0213af577d12cf11a5baf5a869e0b1305684ca0a"

h1_start_node = (f"nohup geth --metrics --rpc --datadir=$DDR1 --networkid {network_id} "
                 f"--nat extip:{bootnode_ip} --netrestrict 10.0.0.0/24 --port {bootnode_port} &")
h2_gen_enode = (f"ENODE_ADDRESS=\"enode://$(bootnode -nodekey $DDR1/geth/nodekey "
                f"-writeaddress)@{bootnode_ip}:{bootnode_port}\"")
h2_start_node = (f"nohup geth --metrics --rpc --datadir $DDR2 --networkid {network_id} "
                 f"--port {bootnode_port + 1} --bootnodes $ENODE_ADDRESS > nohup2.out &")
h2_check_join = "geth attach $DDR2/geth.ipc --exec admin.peers"
h3_start_mine = (f"nohup geth --metrics --rpc --datadir $DDR3 --networkid {network_id} "
                 f"--port {bootnode_port + 2} --mine --minerthreads=1 --etherbase={miner_base} > nohup3.out &")
h3_check_mine = "geth attach $DDR3/geth.ipc --exec 'web3.fromWei(eth.getBalance(eth.coinbase), \"ether\")'"
h3_clean_up = "killall geth"
