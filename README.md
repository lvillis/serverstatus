<h1 align="center">
    <br>ServerStatus<br>
</h1>
<p align="center">
    <em>云探针、多服务器探针、云监控、多服务器云监控、定时任务监控</em>
</p>
<p align="center">
    <a href="https://github.com/lvillis/serverstatus">
        <img src="https://img.shields.io/badge/Python-3.9-blue.svg" alt="Python Support">
    </a>
    <a href="https://github.com/lvillis/serverstatus">
        <img src="https://img.shields.io/badge/Vue-3-blue.svg?" alt="Vue Support">
    </a>
    <a href="https://github.com/lvillis/serverstatus">
        <img src="https://img.shields.io/github/license/lvillis/ServerStatus?style=flat-square" alt="License">
    </a>
    <a href="https://github.com/lvillis/serverstatus">
        <img src="https://img.shields.io/github/repo-size/lvillis/ServerStatus?style=flat-square&color=328657" alt="GitHub repo size">
    </a>
    <a href="https://github.com/lvillis/serverstatus">
        <img src="https://img.shields.io/github/last-commit/lvillis/serverstatus.svg?label=commits" alt="GitHub last commit">
    </a>
</p>


---
## <a href="https://github.com/lvillis/serverstatus">Demo</a>
## Features

* 检测服务器IPv4&IPv6的连通性，共存则显示双栈
* 依据 Load 与 CPU Cores 的数值在Load栏显示不同背景色
* ServerStatus下拉栏增加更多数据
* 增加HealthCheck，检测定时任务的执行情况

## TODO

- [ ] 异常通知

---

## Server [![Github Actions](https://img.shields.io/github/workflow/status/lvillis/serverstatus/Docker?style=flat-square)](https://github.com/Dreamacro/clash/actions) [![Docker Image Size (tag)](https://img.shields.io/docker/image-size/lvillis/serverstatus/server)](https://hub.docker.com)

```
docker run -d \
    --name=serverstatus-server \
    -p 35601:35601 \
    -v /root/ServerStatus/server/config.json:/root/src/config.json \
    -v /etc/localtime:/etc/localtime:ro \
    --restart=always lvillis/serverstatus:server
```

## Dashboard [![Github Actions](https://img.shields.io/github/workflow/status/lvillis/serverstatus/Docker?style=flat-square)](https://github.com/Dreamacro/clash/actions) [![Docker Image Size (tag)](https://img.shields.io/docker/image-size/lvillis/serverstatus/dashboard)](https://hub.docker.com)

```
docker run -d \
    --name=serverstatus-dashboard \
    -p 8080:80 \
    -e API_URL="http://127.0.0.1:35601/get" \
    --restart=always lvillis/serverstatus:dashboard
```

## Agent [![Github Actions](https://img.shields.io/github/workflow/status/lvillis/serverstatus/Docker?style=flat-square)](https://github.com/Dreamacro/clash/actions) [![Docker Image Size (tag)](https://img.shields.io/docker/image-size/lvillis/serverstatus/agent)](https://hub.docker.com)

```
docker run -d --privileged --pid=host \
    --name=serverstatus-agent \
    -e API_URL="http://127.0.0.1:35601/post" \
    -e USER=test1 \
    -v /proc:/host/proc \
    -v /etc/localtime:/etc/localtime:ro \
    --restart=always lvillis/serverstatus:agent
```

Agent获取 每月流量 依赖vnstat，centos7安装vnstat最新版如下

```
yum install -y kernel-headers gcc sqlite sqlite-devel
wget https://humdi.net/vnstat/vnstat-latest.tar.gz
tar zxvf vnstat-latest.tar.gz
cd vnstat-*
./configure --prefix=/usr --sysconfdir=/etc
make && make install
sed -i 's/SaveInterval 5/SaveInterval 1/g' "/etc/vnstat.conf"
cp -v examples/systemd/simple/vnstat.service /etc/systemd/system/
systemctl enable vnstat
systemctl start vnstat
```

---

## 相关开源项目:

* ServerStatus：https://github.com/BotoX/ServerStatus
* mojeda's ServerStatus: https://github.com/mojeda/ServerStatus
* BlueVM's project: http://www.lowendtalk.com/discussion/comment/169690#Comment_169690
* Hotaru theme: https://github.com/CokeMine/Hotaru_theme

---

## Special thanks

[![Jetbrains Logo](https://krwu.github.io/img/jetbrains.svg)](https://www.jetbrains.com/?from=serverstatus)

Thanks to [Jetbrains](https://www.jetbrains.com/?from=serverstatus) for supporting this small open source project! I
used Pycharm and WebStorm for years, they are the best tools!