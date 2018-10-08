#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json
import psutil
import socket
import requests


class MemoryMonitor(object):
    def __init__(self):
        self.data = {}

    def getMemorystate(self):  # 监控内存
        phymem = psutil.virtual_memory()

        mem_all = int(phymem.total / 1024 / 1024)  # 总内存,转换为MB单位
        mem_free = int(phymem.free / 1024 / 1024)  # 剩余内存

        cur_mem = mem_all - mem_free  # 当前使用内存

        mem_rate = round((cur_mem/mem_all),2)*100  # 内存使用率,保留2位小数点
        # print(mem_rate)

        struct_time = time.localtime()
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)  # 转换为标准时间
        t = time.time()  # 当前时间戳
        time_stamp = int(round(t * 1000))  # 转换为毫秒的时间戳

        self.data['cur_mem'] = cur_mem
        self.data['mem_rate'] = mem_rate
        self.data['mem_all'] = mem_all
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

    def send(self):
        ip = self.get_host_ip()
        data = self.getMemorystate()  # type:dict
        data['ip'] = ip

        # 发送post请求
        response = requests.post('http://192.168.142.128:8000/api/memory/add/', data=data)
        return response.content


res = MemoryMonitor().send()
result = json.loads(res.decode("utf-8"))  # type:dict

if result.get("error"):
    print("发送失败!", result.get("error"))
else:
    print("发送成功!")
