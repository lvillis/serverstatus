import asyncio
import json
import time
from concurrent.futures import ThreadPoolExecutor

import requests

from configs import *
from log import logger


class shell:
    @classmethod
    def host(cls, command):
        _command = f'nsenter -t 1 -m -u -n -i -- sh -c "{command}"'
        return os.popen(_command)


def get_uptime():
    command = 'cat /proc/uptime'
    text = shell.host(command).read()

    _uptime = int(float(text.replace('\n', '').split(' ')[0]))
    return _uptime


def get_memory():
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
    return _MemTotal, _MemUsed, _SwapTotal, _SwapFree


def get_disk():
    command = 'df -Tlm --total -t ext4 -t ext3 -t ext2 -t reiserfs -t jfs -t ntfs -t fat32 -t btrs -t fuseblk -t zfs ' \
              '-t simfs -t xfs'
    text = shell.host(command).read()

    _total = text.splitlines()[-1]
    _used = int(_total.split()[3])
    _size = int(_total.split()[2])
    return _size, _used


def get_load():
    command = "cat /proc/loadavg"
    text = shell.host(command).read()

    text = text.split(' ')
    load_1 = float(text[0])
    load_5 = float(text[1])
    load_15 = float(text[2])
    return load_1, load_5, load_15


def get_cpu():
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
    return round(result, 1)


def get_bandwidth():
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
        return _NET_IN, _NET_OUT
    if version >= 2.6:
        command = 'vnstat --json'
        text = shell.host(command).read()
        vnstat_json = json.loads(text)
        month_rx = vnstat_json['interfaces'][-1]['traffic']['month'][-1]['rx']
        month_tx = vnstat_json['interfaces'][-1]['traffic']['month'][-1]['tx']
        return month_rx, month_tx


network_dict = {
    'online4': False,
    'online6': False
}


def get_network():
    while True:
        command = "ping -B -w 2 -n -c 2 ipv4.google.com"
        text = shell.host(command).read()
        if 'rtt' in text:
            network_dict['online4'] = True
        else:
            network_dict['online4'] = False

        command = "ip -f inet6 -o addr show"
        text = shell.host(command).read()
        if len(text) == 0:
            network_dict['online6'] = False
        else:
            command = "ping6 -B -w 2 -n -c 2 ipv6.google.com"
            text = shell.host(command).read()
            if 'rtt' in text:
                network_dict['online6'] = True
            else:
                network_dict['online6'] = False
            time.sleep(INTERVAL)


traffic_dict = {
    'netrx': 0.0,
    'nettx': 0.0,
    'clock': 0.0,
    'diff': 0.0,
    'avgrx': 0,
    'avgtx': 0
}


def get_traffic():
    command = 'cat /proc/net/dev'
    while True:
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
        time.sleep(INTERVAL)


def get_tupd():
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
    return int(_tcp), int(_udp), int(_process), int(_thread)


def get_ssh_sessions():
    command = 'who | wc -l'
    text = shell.host(command).read()

    ssh_sessions = text.replace('\n', '')
    return int(ssh_sessions)


def get_kernel():
    command = 'uname -r'
    text = shell.host(command).read()

    kernel = text.replace('\n', '')
    return str(kernel)


def get_tcp_cc():
    command = 'sysctl net.ipv4.tcp_congestion_control'
    text = shell.host(command).read()

    tcp_cc = text.replace('\n', '').replace(' ', '').split('=')[1]
    return str(tcp_cc)


def get_cpu_info():
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

    return cpu_model, cpu_cores, cpu_speed


status_json = {}


def get_status():
    while True:
        cpu = get_cpu()
        net_in, net_out = get_bandwidth()
        uptime = get_uptime()
        load_1, load_5, load_15 = get_load()
        memory_total, memory_used, swap_total, swap_free = get_memory()
        disk_total, disk_used = get_disk()
        tcp_count, udp_count, process_count, thread_count = get_tupd()
        cpu_model, cpu_cores, cpu_speed = get_cpu_info()

        status_json['username'] = USER
        status_json['online4'] = network_dict['online4']
        status_json['online6'] = network_dict['online6']
        status_json['uptime'] = uptime
        status_json['load_1'] = load_1
        status_json['load_5'] = load_5
        status_json['load_15'] = load_15
        status_json['memory_total'] = memory_total
        status_json['memory_used'] = memory_used
        status_json['swap_total'] = swap_total
        status_json['swap_used'] = swap_total - swap_free
        status_json['hdd_total'] = disk_total
        status_json['hdd_used'] = disk_used
        status_json['cpu'] = cpu
        status_json['network_rx'] = traffic_dict.get("netrx")
        status_json['network_tx'] = traffic_dict.get("nettx")
        status_json['network_in'] = net_in
        status_json['network_out'] = net_out
        status_json['tcp_count'] = tcp_count
        status_json['udp_count'] = udp_count
        status_json['process_count'] = process_count
        status_json['thread_count'] = tcp_count
        status_json['ssh_sessions'] = get_ssh_sessions()
        status_json['kernel'] = get_kernel()
        status_json['tcp_cc'] = get_tcp_cc()
        status_json['cpu_model'] = cpu_model
        status_json['cpu_cores'] = cpu_cores
        status_json['cpu_speed'] = cpu_speed
        status_json['update_time'] = int(time.time())

        logger.info(status_json)
        time.sleep(0.1)


def send_data():
    session = requests.Session()
    while True:
        try:
            ret = session.post(API_URL, json=status_json, timeout=2)
            logger.info(ret.status_code)
        except:
            logger.error("Webapi Error")
        finally:
            time.sleep(INTERVAL)


async def main_thread():
    with ThreadPoolExecutor(max_workers=5) as pool:
        loop = asyncio.get_running_loop()
        futures = [
            loop.run_in_executor(pool, get_traffic),
            loop.run_in_executor(pool, get_network),
            loop.run_in_executor(pool, get_status),
            loop.run_in_executor(pool, send_data),
        ]
        await asyncio.gather(*futures, return_exceptions=False)


if __name__ == '__main__':
    asyncio.run(main_thread())
