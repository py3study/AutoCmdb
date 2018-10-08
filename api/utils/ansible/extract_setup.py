#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
解析setup信息,提取相关硬件信息,方便入库
"""

class extract(object):
    """
    提取有效数据
    """
    def __init__(self,ip,data):
        self.ip = ip
        self.data = data

    def get_disk(self,info):
        """
        获取磁盘信息
        :param info:
        :return: []
        """
        d = "xvbs"  # 硬盘设备名的开头字母

        dic1 = {}

        for i in info:
            for j in d:
                if i.startswith(j):  # 判断是否以指定字母开头
                    # print(i)  # 比如sda
                    dic1[i] = info[i]  # 添加到空字典中


        # sr0是CD - ROM驱动器，要删除掉
        if dic1.get('sr0'):
            dic1.pop('sr0')

        li = []
        for i in dic1:
            li.append({'device_name': i, 'disk_type': dic1[i]['host'].split()[0], 'disk_size': dic1[i]['size']})

        return li

    def network_card(self,network_list):
        """
        获取网卡信息
        :param ip:  ip地址
        :param network_list:  网卡列表
        :return: []
        """
        li = []
        for i in network_list:
            network_name = i  # 网卡名
            ipaddr = self.data[self.ip]['ansible_facts']["ansible_" + i]['ipv4']['address']  # ip地址
            netmask = self.data[self.ip]['ansible_facts']["ansible_" + i]['ipv4']['netmask']  # 子网掩码
            network = self.data[self.ip]['ansible_facts']["ansible_" + i]['ipv4']['network']  # 网络地址
            # print "ansible_" + i
            mac_addr = self.data[self.ip]['ansible_facts']["ansible_" + i]['macaddress']  # mac地址
            tape_width = self.data[self.ip]['ansible_facts']["ansible_" + i]['module']  # 网卡带宽
            bandwidth = tape_width.replace('e', 'Ethernet ')  # 将字母e替换为Ethernet
            bandwidth = bandwidth + "Mbps"

            active = self.data[self.ip]['ansible_facts']["ansible_" + i]['active']  # 是否激活

            # 以上信息添加到列表中
            li.append({'network_name': network_name, 'ipaddr': ipaddr, 'netmask': netmask, 'network': network,
                       'mac_addr': mac_addr, 'bandwidth': bandwidth, 'active': active})

        return li

    def bytes_conversion(self,number):
        """
        流量单位转换
        :param number: int
        :return: xx k/m/g/...
        """
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = dict()
        for i, s in enumerate(symbols):
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if int(number) >= prefix[s]:
                value = float(number) / prefix[s]
                return '%.2f %s' % (value, s)
        return "%s B" % number

    def get_info(self):
        """
        获取指定IP的硬件信息
        :param ip: ip地址
        :return: dict
        """
        sn = self.data[self.ip]['ansible_facts']['ansible_product_serial']
        host_name = self.data[self.ip]['ansible_facts']['ansible_hostname']
        # 操作系统
        description = self.data[self.ip]['ansible_facts']['ansible_distribution']
        # 系统版本
        distribution_version = self.data[self.ip]['ansible_facts']['ansible_distribution_version']
        # 系统位数
        ansible_machine = self.data[self.ip]['ansible_facts']['ansible_machine']
        # 系统信息
        sysinfo = '%s %s' % (distribution_version, ansible_machine)
        # 系统内核
        os_kernel = self.data[self.ip]['ansible_facts']['ansible_kernel']
        # cpu型号
        cpu_model = self.data[self.ip]['ansible_facts']['ansible_processor'][2]
        # cpu线程数
        # cpu_count = datastructure[ip]['ansible_facts']['ansible_processor_count']
        # cpu核心数
        cpu_cores = self.data[self.ip]['ansible_facts']['ansible_processor_cores']
        ###############################
        # 内存容量,单位MB
        mem = self.data[self.ip]['ansible_facts']['ansible_memtotal_mb']

        switch_bytes = mem * 1024 * 1024  # 还原为字节
        res = self.bytes_conversion(switch_bytes)  # 转换单位

        num, unit = res.split()  # 切割字符串
        memory = round(float(num))  # 数字向上取整
        real_memory = '{} {}'.format(memory,unit)
        # print(num, unit)
        ################################
        # 磁盘信息
        disk = self.get_disk(self.data[self.ip]['ansible_facts']['ansible_devices'])

        # 构造字典
        res = {}
        res['hostname'] = host_name
        res['cpu'] = cpu_cores
        res['memory'] = real_memory
        res['os'] = description

        res['cpu_info'] = cpu_model
        res['kernel'] = os_kernel
        res['sn'] = sn
        res['os_version'] = sysinfo

        res['disk'] = disk
        network_list = self.data[self.ip]['ansible_facts']['ansible_interfaces']
        network_list_new = []
        for i in network_list:
            if i != 'lo':  # 剔除掉lo网卡
                network_list_new.append(i)

        res['network_name'] = network_list_new

        res['network_card'] = self.network_card(network_list_new)  # 网卡信息

        return res
