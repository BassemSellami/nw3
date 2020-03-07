import yaml
import pprint

conf = yaml.load(open("config.yaml"))


def pre_process():
    assert (conf["nw_iperf_mode"] in [-1, 0, 1],
            "nw_iperf_mode should = -1 | 0 | 1")
    if "args" not in conf["nw_topo"]:
        conf["nw_topo"]["args"] = []
    if "kwargs" not in conf["nw_topo"]:
        conf["nw_topo"]["kwargs"] = {}


def get_node_params():
    return conf["nw_node_param"]


def get_link_params():
    return conf["nw_link_param"]


pre_process()
pprint.pprint(conf)
