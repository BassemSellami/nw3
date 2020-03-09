from sys import modules
from os import system
from functools import partial
from topos import *
from geth import *
from conf import conf
from time import sleep
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
import subprocess


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
    delay_command(2, h2_gen_enode)
    delay_command(2, h2_start_node)
    sleep(2)
    delay_command(2, h2_check_join)
    delay_command(3, h3_start_mine)
    for i in range(20):
        print("i =", i)
        delay_command(3, h3_check_mine)
    delay_command(3, h3_clean_up)

    # enables client control
    # CLI(net)

    # stop the network
    net.stop()


if __name__ == '__main__':
    main()
