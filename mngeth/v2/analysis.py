from pprint import pprint
import re
import datetime


def read_file(file):
    with open(file) as f:
        return f.readlines()


def find_max_valid_block(raw_logs):
    num = 0
    for raw_log in raw_logs:
        for line in raw_log[::-1]:
            if "🔗 block reached canonical chain " in line:
                cnum = int(line.split()[-2].split("=")[-1])
                if cnum > num:
                    num = cnum
    if num == 0:
        raise Exception
    else:
        return num


def extract_time(time_raw="[04-11|14:39:58.449]"):
    time_arr = re.split("[\[Srw\-|:.\]]", time_raw)[1:-1]
    time_arr = [int(i) for i in time_arr]
    time_arr[-1] = time_arr[-1] * 1000
    assert len(time_arr) == 6
    time_dt = datetime.datetime(2020, *time_arr)
    return time_dt.timestamp()


def extract_history(nodes, raw_logs, max_valid_block_num):
    histories = []
    for block_num in range(max_valid_block_num):
        histories.append([])
        for node_num, raw_log in enumerate(raw_logs):
            for line in raw_log:
                if f" number={block_num} " in line:
                    histories[block_num].append(nodes[node_num] + "\t" + line.strip())
    for i in range(max_valid_block_num):
        histories[i] = sorted(histories[i], key=lambda s: s.split()[2] + s.split()[0])
    return histories


def print_block_hist_info(histories, info_arr, num):
    print()
    print()
    print("block number = ", num)
    print("total log entries = ", len(histories[num]))
    print(info_arr[num])
    print()
    for line in histories[num]:
        print(line)


def extract_info(histories, max_valid_block_num):
    info_arr = []
    for num in range(max_valid_block_num):
        info = {"num": num}

        for line in histories[num]:
            if "🔗 block reached canonical chain " in line:
                info["hash"] = line.split()[-1].split()[-1]
                info["sender_recv_time"] = extract_time(line.split()[2])

        for line in histories[num]:
            if "🔨 mined potential block " in line and info["hash"] in line:
                info["sender"] = line.split()[0]
                info["sender_send_time"] = extract_time(line.split()[2])
            elif "Imported new chain segment " in line and info["hash"] in line and "10.0.0.1" in line:
                info["boot_recv_time"] = extract_time(line.split()[2])

        if len(list(info.keys())) == 6:
            info["valid"] = True
        else:
            info["valid"] = False
        info_arr.append(info)

    return info_arr


def calculate_metrics(nodes, info_arr):
    pass
    # definitions
    # sender_send_time: the system time that a miner reports it has mined a potential block
    # sender_recv_time: the system time that a miner reports its block has reached the canonical chain
    # boot_recv_time: the system time that the bootnode reports it has receives a block to the chain

    # what do I mean by a valid block: a block that has the above time recorded in logs

    # when two miners produce their i-th blocks at around the same time,
    # only one miner reports its block (say, with hash A) has reached the canonical chain
    # so sender_send_time, sender_recv_time, boot_recv_time are all related to the block with hash A
    # (so another miner's send time is ignored in this version)

    # this method calculates & returns
    # 1) bootnode's throughput: a float, equals to
    # the total # of valid blocks / ((last valid block's boot_recv_time) - (first valid block's sender_send_time))
    # 2) bootnode's latencies: an array of floats,
    # i-th element stores (i-th valid block's boot_recv_time - sender_send_time)
    # note: if some blocks in the middle are not considered as valid,
    # the length of the array may be less than the last valid block's index

    # 3) miner i's throughput: a float, equals to
    # the total # of blocks that 1) considered valid and 2) sent by miner i
    # 4) miner i's latencies: an array of floats,
    # i-th element stores (sender_recv_time - sender_send_time) of i-th block that satisfies 1) and 2)
    # note: the sum lengths of all miner's lantency arrays = the length of the bootnode's latency array

    # 5) cross throughput: a float, equals to
    # the total # of valid blocks / ((last valid block's sender_recv_time) - (first valid block's sender_send_time))
    # 6) cross latencies: an array of floats,
    # i-th element stores i-th valid block's sender_recv_time - sender_send_time
    # note: the length of the cross throughput latency array = the length of the bootnode's latency array

    first_valid, last_valid = None, None
    total_valid_count = 0
    for info in info_arr:
        if info["valid"]:
            total_valid_count += 1
            if first_valid is None:
                first_valid = info
            last_valid = info
    assert first_valid is not None
    assert last_valid is not None
    print(first_valid)
    print(last_valid)
    boot_tho = total_valid_count / (last_valid['boot_recv_time'] - first_valid['sender_send_time'])
    cros_tho = total_valid_count / (last_valid['sender_recv_time'] - first_valid['sender_send_time'])
    # 0th entry: bootnode's throughput
    # 1st entry: cross throughput
    # 2nd entry: minier 1's tho
    # 3rd entry: minier 2's tho
    # ...
    throughputs = [boot_tho, cros_tho]

    for miner in nodes[2:]:
        miner_first_valid, miner_last_valid = None, None
        miner_valid_count = 0
        for info in info_arr:
            if info["valid"] and info["sender"] == miner:
                miner_valid_count += 1
                if miner_first_valid is None:
                    miner_first_valid = info
                miner_last_valid = info
        assert miner_first_valid is not None
        assert miner_last_valid is not None
        # print(miner_first_valid)
        # print(miner_last_valid)
        miner_tho = miner_valid_count / (last_valid['sender_recv_time'] - first_valid['sender_send_time'])
        throughputs.append(miner_tho)

    # print(throughputs)

    boot_lat = []
    cros_lat = []
    for info in info_arr:
        if info["valid"]:
            boot_lat.append(info['boot_recv_time'] - info['sender_send_time'])
            cros_lat.append(info['sender_recv_time'] - info['sender_send_time'])

    latencies = [boot_lat, cros_lat]

    for miner in nodes[2:]:
        miner_lat = []
        for info in info_arr:
            if info["valid"] and info["sender"] == miner:
                miner_lat.append(info['sender_recv_time'] - info['sender_send_time'])
        latencies.append(miner_lat)

    return throughputs, latencies


def report_metrics(nodes, throughputs, latencies):
    pass
    print("report--->")
    for i, tho in enumerate(throughputs):
        if i == 0:
            print("[bootnode]", "throughput", round(tho, 2), "(blocks/sec)")
        elif i == 1:
            print("[cross]", "throughput", round(tho, 2), "(blocks/sec)")
        else:
            print(f"[miner-{nodes[i]}]", "throughput", round(tho, 2), "(blocks/sec)")

    for i, lat in enumerate(latencies):
        if i == 0:
            print("[bootnode]", "latency", "average", round(sum(lat) / len(lat), 2), "(sec)")
            print("[bootnode]", "latency", "median", round(sorted(lat)[int(len(lat) * 0.5)], 2), "(sec)")
            print("[bootnode]", "latency", "95th", round(sorted(lat)[int(len(lat) * 0.95)], 2), "(sec)")
        elif i == 1:
            print("[cross]", "latency", "average", round(sum(lat) / len(lat), 2), "(sec)")
            print("[cross]", "latency", "median", round(sorted(lat)[int(len(lat) * 0.5)], 2), "(sec)")
            print("[cross]", "latency", "95th", round(sorted(lat)[int(len(lat) * 0.95)], 2), "(sec)")
        else:
            print(f"[miner-{nodes[i]}]", "latency", "average", round(sum(lat) / len(lat), 2), "(sec)")
            print(f"[miner-{nodes[i]}]", "latency", "median", round(sorted(lat)[int(len(lat) * 0.5)], 2), "(sec)")
            print(f"[miner-{nodes[i]}]", "latency", "95th", round(sorted(lat)[int(len(lat) * 0.95)], 2), "(sec)")
    print("<---end of the report")

def main():
    # 10.0.0.1 - 10.0.0.4,
    # where 10.0.0.1 is the bootnode,
    # 10.0.0.2 is a follower,
    # and all other nodes are miners
    nodes = [f"10.0.0.{i}" for i in range(1, 5)]
    raw_logs = [read_file(f"./data/nohup-{i}.out") for i in nodes]
    max_valid_block_num = find_max_valid_block(raw_logs) + 1
    histories = extract_history(nodes, raw_logs, max_valid_block_num)
    info_arr = extract_info(histories, max_valid_block_num)

    print(nodes)
    print("len(histories) = ", len(histories))
    print("len(info_arr) = ", len(info_arr))

    # print_block_hist_info(histories, info_arr, 0)
    # print_block_hist_info(histories, info_arr, 1)
    # print_block_hist_info(histories, info_arr, 2)
    tho, lat = calculate_metrics(nodes, info_arr)
    report_metrics(nodes, tho, lat)


main()
