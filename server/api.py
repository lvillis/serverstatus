import datetime
import json
import time
import threading

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crontab import CronTab

from utils import get_local_json

app = FastAPI()

# CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

all_json, servers_list, healthchecks_list = get_local_json()


class status(BaseModel):
    username: str
    online4: bool
    online6: bool
    uptime: str
    load_1: float
    load_5: float
    load_15: float
    network_rx: int
    network_tx: int
    network_in: int
    network_out: int
    cpu: int
    memory_total: int
    memory_used: int
    swap_total: int
    swap_used: int
    hdd_total: int
    hdd_used: int
    tcp_count: int
    udp_count: int
    process_count: int
    thread_count: int
    ssh_sessions: int
    kernel: str
    tcp_cc: str
    cpu_model: str
    cpu_cores: int
    cpu_speed: float
    update_time: int


@app.post("/post")
async def post(data: status):
    # TODO: server time == client time ?

    remote_json = json.loads(data.json())

    find_username = False
    for idx, server in enumerate(servers_list):
        # 获取本地username
        local_username = server['username']

        # 判断username是否存在
        if local_username != remote_json['username']:
            continue

        # 添加本地字段至remote_json
        remote_json['name'] = server['name']
        remote_json['host'] = server['host']
        remote_json['location'] = server['location']
        remote_json['type'] = server['type']

        # 格式化时间
        uptime = int(remote_json['uptime'])
        uptime_day = uptime / 60 / 60 / 24
        if uptime_day >= 1:
            remote_json['uptime'] = f"{int(uptime_day)} 天"
        else:
            remote_json['uptime'] = str(datetime.timedelta(seconds=uptime))

        # 添加remote_json至all_json
        servers_list[idx] = remote_json
        find_username = True

    if find_username:
        # 添加更新时间 updated
        all_json['updated'] = int(time.time())
        return all_json
    else:
        return {'message': 'not found username'}


@app.get("/get")
async def get():
    # 添加更新时间 updated
    all_json['updated'] = int(time.time())
    return all_json


def get_next_time(value):
    # 延迟时间 x秒后执行 crontab 任务
    delay_time = CronTab(value).next(default_utc=False)
    # 下次执行时间的时间戳
    next_time_timestamp = int(time.time() + delay_time)
    # 转换成localtime
    time_local = time.localtime(next_time_timestamp)
    # 转换成新的时间格式(2026-05-05 20:28:54)
    next_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return next_time, next_time_timestamp


@app.get("/hc/{token}")
async def get(token):
    return_msg = None
    remote_token = token
    for idx, check in enumerate(healthchecks_list):
        # 获取本地 token
        local_token = check['token']

        # 判断 token 是否存在
        if local_token != remote_token:
            return_msg = 'Token Error'
            continue
        else:
            # 解析 contab 表达式 生成 next_time
            next_time, next_time_timestamp = get_next_time(check['period'])

            check['next_time']: str = next_time
            check['next_time_timestamp']: int = next_time_timestamp

            check['last_ping_timestamp'] = int(time.time())
            check['status']: str = 'success'
            return_msg = 'Pong!'
            break
    return return_msg


def healthcheck_thread():
    while True:
        for idx, check in enumerate(healthchecks_list):
            # 判断是否存在last_ping_timestamp 即 是否成功ping 并生成数据
            has_last_ping_time = check.__contains__('last_ping_timestamp')
            if not has_last_ping_time:
                check['last_ping']: str = 'Never'
                check['status']: str = 'Never'
                continue

            # 计算last_ping  现在时间-上次执行时间
            last_ping = int(time.time()) - check['last_ping_timestamp']
            last_ping = str(datetime.timedelta(seconds=last_ping))
            check['last_ping'] = f"{last_ping} ago"

            # 超时设置
            if (time.time() > check['next_time_timestamp']
                    and time.time() - check['next_time_timestamp'] > int(check['grace']) * 60):
                check['status']: str = 'error'

        time.sleep(1)


def serverstatus_thread():
    while True:
        for idx, server in enumerate(servers_list):
            # 判断是否存在update_time 即 是否连接过服务端
            has_last_update_time = server.__contains__('update_time')
            # 未连接则跳过
            if not has_last_update_time:
                continue
            # 超时设置
            if int(time.time()) - server['update_time'] > 5:
                server['online4'] = False
                server['online6'] = False
        time.sleep(1)


threading.Thread(target=healthcheck_thread).start()
threading.Thread(target=serverstatus_thread).start()
