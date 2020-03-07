from sys import modules
from os import system
from rmb.topos import *


def get_topology():
    try:
        topo_cls = getattr(modules[__name__], conf["nw_topo"]["class"])
        topo_obj = topo_cls(*conf['nw_topo']["args"], **conf['nw_topo']["kwargs"])
        net = Mininet(topo=topo_obj, host=CPULimitedHost, link=TCLink)
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


def read_count():
    stats_file = "watch.txt"
    with open(stats_file) as f:
        lines = f.read().count("Successful")
    return lines


def main():
    server_cnt = 5

    old_lines = read_count()

    system('sudo mn --clean')
    setLogLevel('info')

    # reads YAML configs and creates the network
    topo, net = get_topology()
    net.start()

    # tests connections (include iperf)
    test_topology(topo, net)

    # hs = topo.hosts(sort=True)
    # hs = [net.getNodeByName(h) for h in hs]
    # for h in hs[::-1]:
    #     h.cmdPrint("export GOPATH=~/go/goworkspace")
    #     h.cmdPrint("cd ~/go/goworkspace/src/HRB/ && ls")
    #     h.cmdPrint("go run main.go >> ~/nw3/watch.txt &")
    #     h.cmdPrint("ls")
    #
    # while True:
    #     new_lines = read_count()
    #     if new_lines == old_lines + server_cnt:
    #         break
    #     print("sleep 5 secs, bc oldcurrent new_lines = ", new_lines)
    #     sleep(5)

    # enables client control
    CLI(net)

    # stop the network
    net.stop()


if __name__ == '__main__':
    main()
