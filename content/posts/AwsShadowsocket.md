---
blog_cover:
- /bi/aws_change_port_1.png
date: 2023-03-10
tags:
- AWS
- instance
- Shadowsocket
title: Aws Shadowsocket
weight: 15
---

keyword: AWS instance


![image#width=50%](/bi/aws_instance_name.png)

创建key 用于 ssh 鉴权登陆

![image#width=50%](/bi/aws_instance_create_key.png)

创建成功后，查看instance Details ip , ssh 登陆

```
chmod 400 [your pem path]
ssh -i [your pem path] admin@your_ip
```

安装 [shadowsocket docker](https://github.com/shadowsocks/shadowsocks-libev/blob/master/docker/alpine/README.md)


```
docker pull shadowsocks/shadowsocks-libev
```

指定 shadowsocks container 的端口，检查你的云服务是否开启了该端口
启动 docker instance
检查你的云服务是否开启了该端口

![image#width=50%](/bi/aws_instance_check_port.png)

```
ps=<你的密码>
port=<你的端口>

docker run -e PASSWORD=$ps -p $port:8388 -p $port:8388/udp -d --restart always shadowsocks/shadowsocks-libev
```

![image#width=50%](/bi/aws_change_port_1.png)

![image#width=50%](/bi/aws_change_port_2.png)