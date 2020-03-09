from sys import modules
from os import system
from functools import partial
from topos import *
from conf import conf
from time import sleep
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
import subprocess

h1_start_node = "geth --datadir=$DDR1 --networkid 714714 --nat extip:10.0.0.1 --netrestrict 10.0.0.0/24 --port 30303 &"
h1_gen_bootkey = "geth attach $DDR1/geth.ipc --exec admin.nodeInfo.enr | tr -d '\"' >~/boot.key"
h2_exp_bootkey = "export BT=$(cat ~/boot.key)"
h2_start_node = "geth --datadir $DDR2 --networkid 714714 --port 30304 --bootnodes $BT &"
h2_check_join = "geth attach $DDR2/geth.ipc --exec admin.peers"
h3_start_mine = "geth --datadir $DDR3 --networkid 714714 --port 30307 --mine --minerthreads=1 --etherbase=0x0213af577d12cf11a5baf5a869e0b1305684ca0a &"
h3_check_mine = "geth attach $DDR3/geth.ipc --exec 'web3.fromWei(eth.getBalance(eth.coinbase), \"ether\")'"
h3_clean_up = "killall geth"


def get_topology():
    # privateDirs = [('~/.ethereum', '~/%(name)s/.ethereum')]
    privateDirs = []
    host = partial(CPULimitedHost, privateDirs=privateDirs)
    try:
        topo_cls = getattr(modules[__name__], conf["nw_topo"]["class"])
        topo_obj = topo_cls(*conf['nw_topo']["args"], **conf['nw_topo']["kwargs"])
        net = Mininet(topo=topo_obj, host=host, link=TCLink)
        return topo_obj, net
    except Exception as e:
        print("Specified topology not found: ", e)
        exit(0)


def test_topology(topo: Topo, net: Mininet):
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Waiting switch connections")
    net.waitConnected()

    print("Testing network connectivity - (i: switches are learning)")
    net.pingAll()
    print("Testing network connectivity - (ii: after learning)")
    net.pingAll()

    print("Get all hosts")
    print(topo.hosts(sort=True))

    # print("Get all links")
    # for link in topo.links(sort=True, withKeys=True, withInfo=True):
    #     pprint(link)
    # print()

    if conf['nw_iperf_mode'] == -1:
        return
    hosts = [net.get(i) for i in topo.hosts(sort=True)]
    if conf['nw_iperf_mode'] == 0:
        net.iperf((hosts[0], hosts[-1]))
    elif conf['nw_iperf_mode'] == 1:
        [net.iperf((i, j)) for i in hosts for j in hosts if i != j]


def main():
    def delay_command(host, cmd):
        sleep(1)
        hs[host - 1].cmdPrint(cmd)
        sleep(1)

    system('sudo mn --clean')
    setLogLevel('info')
    system("chmod 700 ./rerun.sh")
    subprocess.call(['./rerun.sh'])

    # reads YAML configs and creates the network
    topo, net = get_topology()
    net.start()

    # tests connections (include iperf)
    test_topology(topo, net)

    hs = topo.hosts(sort=True)
    hs = [net.getNodeByName(h) for h in hs]
    for h in hs[::-1]:
        h.cmdPrint("cd ~")
        h.cmdPrint("ls")


    delay_command(1, h1_start_node)
    delay_command(1, h1_gen_bootkey)
    # delay_command(2, h2_exp_bootkey)
    # delay_command(2, h2_start_node)
    # sleep(5)
    # delay_command(2, h2_check_join)
    # delay_command(3, h3_start_mine)
    # for i in range(120):
    #     delay_command(3, h3_check_mine)
    # delay_command(3, h3_clean_up)

    # enables client control
    CLI(net)

    # stop the network
    net.stop()


if __name__ == '__main__':
    main()
