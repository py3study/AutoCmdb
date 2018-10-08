#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
/etc/ansible/hosts 文件管理
数据库有变动时,查询目前的数据库记录。
将查询的结果转换为字典,重写/etc/ansible/hosts
"""
# from configparser import ConfigParser
from api.utils.response import BaseResponse


class FM(object):  # 文件管理
    def __init__(self,queryset):
        self.queryset = queryset
        self.hosts = '/etc/ansible/hosts'
        self.res = BaseResponse()

    # def dict_result(self):
    #     """
    #     将ansible的主机配置文件转换为字典
    #     :return: dict
    #     {'web': ['192.168.142.129', '192.168.142.131']}
    #     """
    #     dict_result = {}
    #     cf = ConfigParser(allow_no_value=True)
    #     cf.read(self.hosts)
    #     secs = cf.sections()
    #     for sec in secs:
    #         dict_result[sec] = cf.options(sec)
    #
    #     # print(json.dumps(dict_result))
    #     # print(dict_result)
    #     return dict_result


    def queryset_dict(self):
        # queryset = models.AnsibleGroup.objects.all()
        # {'web': ['192.168.142.129', '192.168.142.131']}
        # li = []  # 总列表
        dic = {}
        for i in self.queryset:
            dic[i.name] = []  # 定义空列表,比如: {'web':[]}
            for j in i.ansiblehost_set.all():
                dic[i.name].append(j.ip)  # 将ip写入到列表中

        # li.append(dic)  # 将字典写入到总列表中
        return dic

    def write(self):
        """
        将数据库的记录重新写入ansible的主机配置文件
        是直接覆盖
        :return:
        """
        # dic = {'app': ['192.168.10.129', '192.168.10.131'], 'web': ['192.168.142.129', '192.168.142.131']}
        dic = self.queryset_dict()

        try:
            # 写入配置文件
            with open(self.hosts, 'w', encoding="utf-8") as f:
                for group in dic:
                    # 写入组名,比如[web]
                    f.write('[{}]'.format(group) + "\n")
                    for ip in dic[group]:
                        # 写入ip,比如192.168.10.129
                        f.write(ip + "\n")

                    f.write("\n")  # 末尾再加一个换行符

            return self.res.__dict__

        except Exception as e:
            print(e)
            self.res.code = 500
            self.res.error = "写入/etc/ansible/hosts失败"
            return self.res.__dict__