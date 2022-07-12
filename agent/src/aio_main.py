import asyncio
import inspect
import json
import time
import threading

import requests

from configs import *
from log import logger


class shell:
    @classmethod
    def host(cls, command):
        _command = f'nsenter -t 1 -m -u -n -i -- sh -c "{command}"'
        return os.popen(_command)

    @classmethod
    def local(cls, command):
        ret = os.popen(command)
        return ret


status_json = {}


def get_uptime():
    print(inspect.stack()[0][3])
    command = 'cat /proc/uptime'
    text = shell.host(command).read()

    _uptime = int(float(text.replace('\n', '').split(' ')[0]))
    status_json['uptime'] = _uptime


def get_memory():
    print(inspect.stack()[0][3])
    command = 'cat /proc/meminfo'
    text = shell.host(command).readlines()

    res = dict()
    for line in text:
        text = line.replace('/n', '').replace(' ', '').replace('kB', '').split(':')
        key = str(text[0])
        value = int(text[1])
        res[key] = value
    _MemTotal = res['MemTotal']
    _MemUsed = _MemTotal - res['MemFree'] - res['Buffers'] - res['Cached'] - res['SReclaimable']
    _SwapTotal = res['SwapTotal']
    _SwapFree = res['SwapFree']

    status_json['memory_total'] = _MemTotal
    status_json['memory_used'] = _MemUsed
    status_json['swap_total'] = _SwapTotal
    status_json['swap_used'] = _SwapTotal - _SwapFree


def get_disk():
    print(inspect.stack()[0][3])
    command = 'df -Tlm --total -t ext4 -t ext3 -t ext2 -t reiserfs -t jfs -t ntfs -t fat32 -t btrs -t fuseblk -t zfs ' \
              '-t simfs -t xfs'
    text = shell.host(command).read()

    _total = text.splitlines()[-1]
    _used = int(_total.split()[3])
    _size = int(_total.split()[2])

    status_json['hdd_total'] = _size
    status_json['hdd_used'] = _used


def get_load():
    print(inspect.stack()[0][3])
    command = "cat /proc/loadavg"
    text = shell.host(command).read()

    text = text.split(' ')
    load_1 = float(text[0])
    load_5 = float(text[1])
    load_15 = float(text[2])

    status_json['load_1'] = load_1
    status_json['load_5'] = load_5
    status_json['load_15'] = load_15


def get_cpu():
    print(inspect.stack()[0][3])
    def get_time():
        command = 'cat /proc/stat'
        text = shell.host(command).readline()
        time_list = text.split(' ')[2:6]
        time_list = list(map(int, time_list))
        return time_list

    def delta_time():
        x = get_time()
        time.sleep(INTERVAL)
        y = get_time()
        for i in range(len(x)):
            y[i] -= x[i]
        return y

    t = delta_time()
    st = sum(t)
    if st == 0:
        st = 1
    result = 100 - (float(t[len(t) - 1]) * 100.00 / st)

    status_json['cpu'] = round(result, 1)


def get_bandwidth():
    print(inspect.stack()[0][3])
    command = 'vnstat --version'
    text = shell.host(command).read().split(' ')
    version = float(text[1])
    if version == 1.15:
        command = 'vnstat --dumpdb'
        text = shell.host(command).readlines()

        _NET_IN, _NET_OUT = 0, 0
        for line in text:
            if line[0:4] == "m;0;":
                mdata = line.split(";")
                _NET_IN = int(mdata[3]) * 1024 * 1024
                _NET_OUT = int(mdata[4]) * 1024 * 1024
                break
        status_json['network_in'] = _NET_IN
        status_json['network_out'] = _NET_OUT
    if version >= 2.6:
        command = 'vnstat --json'
        text = shell.host(command).read()
        vnstat_json = json.loads(text)
        month_rx = vnstat_json['interfaces'][-1]['traffic']['month'][-1]['rx']
        month_tx = vnstat_json['interfaces'][-1]['traffic']['month'][-1]['tx']
        status_json['network_in'] = month_rx
        status_json['network_out'] = month_tx


network_dict = {
    'online4': False,
    'online6': False
}


def get_network():
    print(inspect.stack()[0][3])
    command = "ping -B -w 2 -n -c 2 ipv4.google.com"
    text = shell.host(command).read()
    if 'rtt' in text:
        status_json['online4'] = True
    else:
        status_json['online4'] = False
    command = "ping6 -B -w 2 -n -c 2 ipv6.google.com"
    text = shell.host(command).read()
    if 'rtt' in text:
        status_json['online6'] = True
    else:
        status_json['online6'] = False


traffic_dict = {
    'netrx': 0.0,
    'nettx': 0.0,
    'clock': 0.0,
    'diff': 0.0,
    'avgrx': 0,
    'avgtx': 0
}


def get_traffic():
    print(inspect.stack()[0][3])
    command = 'cat /proc/net/dev'

    _avgrx, _avgtx = 0, 0
    net_dev = shell.host(command).readlines()
    for dev in net_dev[2:]:
        dev = dev.split(':')
        if [True for i in ['lo', 'tun', 'docker', 'veth', 'br-', 'vmbr', 'vnet', 'kube'] if i in dev[0]]:
            continue
        dev = dev[1].split()
        _avgrx += int(dev[0])
        _avgtx += int(dev[8])
    now_clock = time.time()
    traffic_dict["diff"] = now_clock - traffic_dict["clock"]
    traffic_dict["clock"] = now_clock
    traffic_dict["netrx"] = int((_avgrx - traffic_dict["avgrx"]) / traffic_dict["diff"])
    traffic_dict["nettx"] = int((_avgtx - traffic_dict["avgtx"]) / traffic_dict["diff"])
    traffic_dict["avgrx"] = _avgrx
    traffic_dict["avgtx"] = _avgtx

    status_json['network_rx'] = traffic_dict.get("netrx")
    status_json['network_tx'] = traffic_dict.get("nettx")


def get_tupd():
    print(inspect.stack()[0][3])
    """
    tcp, udp, process, thread count: for view ddcc attack
    """

    command = 'ss -t|wc -l'
    _tcp = shell.host(command).read().replace('\n', '')
    command = 'ss -u|wc -l'
    _udp = shell.host(command).read().replace('\n', '')
    command = 'ps -ef|wc -l'
    _process = shell.host(command).read().replace('\n', '')
    command = 'ps -eLf|wc -l'
    _thread = shell.host(command).read().replace('\n', '')

    status_json['tcp_count'] = int(_tcp)
    status_json['udp_count'] = int(_udp)
    status_json['process_count'] = int(_process)
    status_json['thread_count'] = int(_thread)


def get_ssh_sessions():
    print(inspect.stack()[0][3])
    command = 'who | wc -l'
    text = shell.host(command).read()
    ssh_sessions = text.replace('\n', '')

    status_json['ssh_sessions'] = int(ssh_sessions)


def get_kernel():
    print(inspect.stack()[0][3])
    command = 'uname -r'
    text = shell.host(command).read()

    kernel = text.replace('\n', '')

    status_json['kernel'] = str(kernel)


def get_tcp_cc():
    print(inspect.stack()[0][3])
    command = 'sysctl net.ipv4.tcp_congestion_control'
    text = shell.host(command).read()

    tcp_cc = text.replace('\n', '').replace(' ', '').split('=')[1]

    status_json['tcp_cc'] = str(tcp_cc)


def get_cpu_info():
    print(inspect.stack()[0][3])
    command = 'cat /proc/cpuinfo'
    text = shell.host(command).readlines()

    cpu_info = {}
    for line in text:
        text = line.replace('\t', '').replace('\n', '').split(':')
        key = text[0].replace(' ', '_')
        try:
            value = text[1]
        except:
            value = None
        cpu_info[key] = value

    cpu_model = cpu_info['model_name']
    cpu_cores = cpu_info['cpu_cores']
    cpu_speed = cpu_info['cpu_MHz']

    status_json['cpu_model'] = cpu_model
    status_json['cpu_cores'] = cpu_cores
    status_json['cpu_speed'] = cpu_speed


def print_json():
    print(inspect.stack()[0][3])
    print(status_json)


from concurrent.futures import ThreadPoolExecutor


async def aio_main():
    # https://guillotina.readthedocs.io/en/latest/training/asyncio.html
    # https://kimmosaaskilahti.fi/blog/2021-01-03-asyncio-workers/

    with ThreadPoolExecutor(max_workers=14) as pool:
        loop = asyncio.get_running_loop()
        futures = [
            loop.run_in_executor(pool, get_uptime),
            loop.run_in_executor(pool, get_memory),
            loop.run_in_executor(pool, get_disk),
            loop.run_in_executor(pool, get_load),
            loop.run_in_executor(pool, get_cpu),
            loop.run_in_executor(pool, get_bandwidth),
            loop.run_in_executor(pool, get_network),
            loop.run_in_executor(pool, get_traffic),
            loop.run_in_executor(pool, get_tupd),
            loop.run_in_executor(pool, get_ssh_sessions),
            loop.run_in_executor(pool, get_kernel),
            loop.run_in_executor(pool, get_tcp_cc),
            loop.run_in_executor(pool, get_cpu_info),
        ]
        try:
            results = await asyncio.gather(*futures, return_exceptions=False)
        except Exception as ex:
            print("Caught error executing task", ex)

    print(f"Finished processing, got results: {results}")


if __name__ == '__main__':
    while True:
        asyncio.run(aio_main())
        print_json()
        time.sleep(INTERVAL)
