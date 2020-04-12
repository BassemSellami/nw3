from sys import modules
from os import system
from functools import partial
from time import time, sleep

from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

from v2_topos import *
from v2_config import conf
from geth import *


def get_topology():
    # privateDirs = [('~/.ethereum', '~/%(name)s/.ethereum')]
    privateDirs = []
    host = partial(CPULimitedHost, privateDirs=privateDirs)
    try:
        topo_cls = getattr(modules[__name__], conf["topo"]["class"])
        topo_obj = topo_cls(*conf['topo']["args"], **conf['topo']["kwargs"])
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

    if conf['test']['iperf'] == -1:
        return
    else:
        hosts = [net.get(i) for i in topo.hosts(sort=True)]
        if conf['test']['iperf'] == 0:
            net.iperf((hosts[0], hosts[-1]))
        else:
            [net.iperf((i, j)) for i in hosts for j in hosts if i != j]


def main():
    def delay_command(host, cmd, print=True):
        sleep(0.1)
        if print:
            hs[host - 1].cmdPrint(cmd)
        else:
            hs[host - 1].cmd(cmd)
        sleep(0.1)

    system('sudo mn --clean')
    setLogLevel('info')

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

    delay_command(1, node_1_start)
    delay_command(2, gen_enode)
    delay_command(3, gen_enode)
    delay_command(4, gen_enode)
    delay_command(2, node_2_start)
    delay_command(3, node_3_start)
    delay_command(4, node_4_start)
    delay_command(2, node_2_check_join)
    delay_command(3, node_3_check_join)
    delay_command(4, node_4_check_join)

    time1 = time()
    for i in range(300):
        delay_command(1, node_1_check_blocks_alt, False)
        delta = time() - time1
        num = read_get_block()
        throughput = num / delta
        print("i =", i, "total # of blocks = ", num, "throughput = ", round(throughput, 2), "blocks/sec")
        sleep(1)

    time2 = time()
    print("delta = ", time2 - time1)
    # enables client control
    # CLI(net)

    # stop the network
    net.stop()


if __name__ == '__main__':
    main()
