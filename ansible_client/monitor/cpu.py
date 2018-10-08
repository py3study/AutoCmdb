#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json
import psutil
import socket
import requests


class CpuMonitor(object):
    def __init__(self):
        self.data = {}

    def getCPUstate(self):  # 监控cpu
        interval = 1
        cpu = psutil.cpu_percent(interval)  # cpu使用率
        struct_time = time.localtime()
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)  # 转换为标准时间
        t = time.time()  # 当前时间戳
        time_stamp = int(round(t * 1000))  # 转换为毫秒的时间戳

        self.data['cpu'] = cpu
        self.data['create_time'] = create_time
        self.data['time_stamp'] = time_stamp

        return self.data

    def get_host_ip(self):
        """
        查询本机ip地址
        :return: ip
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
            return ip

    def send(self):  # 发送给后端服务器
        ip = self.get_host_ip()
        data = self.getCPUstate()  # type:dict
        data['ip'] = ip

        response = requests.post('http://192.168.142.128:8000/api/cpu/add/', data=data)
        return response.content


res = CpuMonitor().send()
result = json.loads(res.decode("utf-8"))  # type:dict

if result.get("error"):
    print("发送失败!", result.get("error"))
else:
    print("发送成功!")
