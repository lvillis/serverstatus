<div align="center">

# ServerStatus
*With agent, multi-server status monitoring.*

[![](https://img.shields.io/badge/Python-3.9-blue?style=flat-square)](https://github.com/lvillis/serverstatus)
[![](https://img.shields.io/badge/Vue-3-blue?style=flat-square)](https://github.com/lvillis/serverstatus)
[![](https://img.shields.io/github/license/lvillis/serverstatus?style=flat-square)](https://github.com/lvillis/serverstatus)
[![](https://img.shields.io/github/repo-size/lvillis/serverstatus?style=flat-square&color=328657)](https://github.com/lvillis/serverstatus)
[![](https://img.shields.io/github/last-commit/lvillis/serverstatus?style=flat-square&label=commits)](https://github.com/lvillis/serverstatus)
[![](https://img.shields.io/docker/pulls/lvillis/serverstatus?style=flat-square)](https://github.com/lvillis/serverstatus)

</div>

---

| Name | Build | Size |
| :---: | :---: | :---: |
| Server | [![Github Actions](https://img.shields.io/github/workflow/status/lvillis/serverstatus/Docker%20server?style=flat-square)](https://github.com/lvillis/serverstatus/actions) | [![Docker Image Size (tag)](https://img.shields.io/docker/image-size/lvillis/serverstatus/server?style=flat-square)](https://hub.docker.com) |
| Dashboard | [![Github Actions](https://img.shields.io/github/workflow/status/lvillis/serverstatus/Docker%20dashboard?style=flat-square)](https://github.com/lvillis/serverstatus/actions) | [![Docker Image Size (tag)](https://img.shields.io/docker/image-size/lvillis/serverstatus/dashboard?style=flat-square)](https://hub.docker.com) |
| Agent | [![Github Actions](https://img.shields.io/github/workflow/status/lvillis/serverstatus/Docker%20agent?style=flat-square)](https://github.com/lvillis/serverstatus/actions) | [![Docker Image Size (tag)](https://img.shields.io/docker/image-size/lvillis/serverstatus/agent?style=flat-square)](https://hub.docker.com) |


## Demo
https://serverstatus.pages.dev/
## Features

* Check the connectivity of server IPv4&IPv6, if coexistence, it will show dual stack
* Display different background colors in the Load column according to the values ​​of Load and CPU Cores
* Add more data to ServerStatus dropdown
* Add HealthCheck to detect the execution of scheduled tasks

## TODO

- [ ] 异常通知

---

## Server
```
docker run -d \
    --name=serverstatus-server \
    -p 35601:35601 \
    -v /root/ServerStatus/server/config.json:/root/src/config.json \
    -v /etc/localtime:/etc/localtime:ro \
    --restart=always lvillis/serverstatus:server
```

## Dashboard 
```
docker run -d \
    --name=serverstatus-dashboard \
    -p 8080:80 \
    -e API_URL="http://127.0.0.1:35601/get" \
    --restart=always lvillis/serverstatus:dashboard
```

## Agent 
```
docker run -d --privileged --pid=host \
    --name=serverstatus-agent \
    -e API_URL="http://127.0.0.1:35601/post" \
    -e USER=test1 \
    -v /proc:/host/proc \
    -v /etc/localtime:/etc/localtime:ro \
    --restart=always lvillis/serverstatus:agent
```

Agent obtains monthly traffic depends on vnstat.

```
# centos7 installs the latest version of vnstat.
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

## Related open source projects:

* ServerStatus：https://github.com/BotoX/ServerStatus
* mojeda's ServerStatus: https://github.com/mojeda/ServerStatus
  <!-- markdown-link-check-disable-next-line -->
* BlueVM's project: http://www.lowendtalk.com/discussion/comment/169690#Comment_169690
* Hotaru theme: https://github.com/CokeMine/Hotaru_theme

---

## Special thanks

[![Jetbrains Logo](https://krwu.github.io/img/jetbrains.svg)](https://www.jetbrains.com/?from=serverstatus)

Thanks to [Jetbrains](https://www.jetbrains.com/?from=serverstatus) for supporting this small open source project! I
used Pycharm and WebStorm for years, they are the best tools!