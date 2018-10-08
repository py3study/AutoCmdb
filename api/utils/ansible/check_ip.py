#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import ipaddress
import socket


class LegalIP(object):
    def __init__(self,ip):
        self.ip = ip
        self.data = {}

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

    def valid_ip(self):
        """
        验证ip是否有效,比如192.168.1.256是一个不存在的ip
        :return: bool
        """
        try:
            # 判断 python 版本
            if sys.version_info[0] == 2:
                ipaddress.ip_address(self.ip.strip().decode("utf-8"))
            elif sys.version_info[0] == 3:
                # ipaddress.ip_address(bytes(ip.strip().encode("utf-8")))
                ipaddress.ip_address(self.ip)

            return True
        except Exception as e:
            print(e)
            return False

    def check_tcp(self, port=22, timeout=1):
        """
        检测tcp端口,这里主要是检测ssh端口是否开放
        :param ip: ip地址
        :param port: 端口号
        :param timeout: 超时时间
        :return: bool
        """
        flag = False
        try:
            socket.setdefaulttimeout(timeout)  # 整个socket层设置超时时间
            cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            address = (str(self.ip), int(port))
            status = cs.connect_ex((address))  # 开始连接
            cs.settimeout(timeout)

            if not status:
                flag = True

            return flag
        except Exception as e:
            print("error:%s" % e)
            return flag

    def test_parameter(self):
        """
        判断网页传递的ip是否合法
        :return: bool
        """
        if self.ip == self.get_host_ip():
            self.data['error'] = "ip不能是本服务器"
            return self.data

        if not self.valid_ip():
            self.data['error'] = "ip地址不合法"
            return self.data

        # flag = False  # 标志位
        # with open('/etc/ansible/hosts') as f:
        #     for line in f:
        #         line_new = line.strip()
        #         # print(line)
        #         if line_new == self.ip:  # 判断ip是否在ansible文件中
        #             flag = True
        #
        # if not flag:
        #     self.data['error'] = "ip不在ansible的hosts文件中"
        #     return self.data

        if not self.check_tcp():
            self.data['error'] = "ssh端口不可达"
            return self.data

        return self.data





# data = {}
#
#
# def valid_ip(ip):
#     try:
#         #判断 python 版本
#         if sys.version_info[0] == 2:
#             ipaddress.ip_address(ip.strip().decode("utf-8"))
#         elif sys.version_info[0] == 3:
#             # ipaddress.ip_address(bytes(ip.strip().encode("utf-8")))
#             ipaddress.ip_address(ip)
#         return True
#     except Exception as e:
#         print(e)
#         return False
#
#
# def check_tcp(ip, port=22, timeout=1):
#     """
#     检测tcp端口
#     :param ip: ip地址
#     :param port: 端口号
#     :param timeout: 超时时间
#     :return: bool
#     """
#     flag = False
#     try:
#         socket.setdefaulttimeout(timeout)  # 整个socket层设置超时时间
#         cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         address = (str(ip), int(port))
#         status = cs.connect_ex((address))  # 开始连接
#         cs.settimeout(timeout)
#
#         if not status:
#             flag = True
#
#     except Exception as e:
#         print("error:%s" % e)
#         return flag
#
#     return flag
#
#
# def test_parameter(ip):
#     """
#     判断网页传递的ip是否合法
#     :return: bool
#     """
#     if not valid_ip(ip):
#         data['error'] = "ip地址不合法"
#         return data
#
#     flag = False  # 标志位
#     with open('/etc/ansible/hosts') as f:
#         for line in f:
#             line_new = line.strip()
#             # print(line)
#             if line_new == ip:  # 判断ip是否在ansible文件中
#                 flag = True
#
#
#     if not flag:
#         data['error'] = "ip不在ansible的hosts文件中"
#         return data
#
#     if not check_tcp(ip):
#         data['error'] = "ssh端口不可达"
#         return data
#
#     return data