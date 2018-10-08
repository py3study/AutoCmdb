from rest_framework.response import Response
from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from repository import models
from api.utils.response import BaseResponse


from api.serializers.ansible import AnsibleSerializer
from api.utils.serialization_general import SerializedData
from api.utils.auth import Authentication
import json


# ansible相关
from api.utils.ansible.exec_ansible import exec_ansible
from api.utils.ansible.check_ip import LegalIP
from api.utils.ansible.extract_setup import extract
from api.utils.ansible.login_host import LoginLinux
from api.utils.ansible.hosts_fm import FM
# import subprocess
# import time
from django.db import transaction

class AnsibleView(ViewSetMixin, APIView):
    def list(self, request, *args, **kwargs):
        """
        Ansible列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = models.AnsibleGroup.objects.all()
        # print(queryset.values())
        serializer_class = AnsibleSerializer
        data = SerializedData(request, queryset, serializer_class).get_data()
        return HttpResponse(json.dumps(data))

    def add(self, request, *args, **kwargs):
        """
        添加Ansible组名
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        res = BaseResponse()
        group = self.request.data.get('group')  # 表单数据
        if not group:
            res.code = 500
            res.error = "组名不能为空"
            return HttpResponse(json.dumps(res.__dict__))

        has_group = models.AnsibleGroup.objects.filter(name=group)
        if has_group:
            res.code = 500
            res.error = "组名已经存在"
            return HttpResponse(json.dumps(res.__dict__))

        try:
            result = models.AnsibleGroup.objects.create(name=group)
            if not result:
                res.code = 500
                res.error = "添加失败"
                return HttpResponse(json.dumps(res.__dict__))

            res.url = "/web/ansible/list/"
            return HttpResponse(json.dumps(res.__dict__))

        except Exception as e:
            print(e)
            res.code = 500
            res.error = "添加异常"
            return HttpResponse(json.dumps(res.__dict__))


    def add_host(self, request, *args, **kwargs):
        """
        添加ansible组下的主机
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        res = BaseResponse()
        pk = self.request.data.get('pk')  # ansible组id
        host = self.request.data.get('host')  # 主机
        if not host:
            res.code = 500
            res.error = "主机不能为空"
            # return Response(res.__dict__)
            return HttpResponse(json.dumps(res.__dict__))

        # 检测ip是否合格
        data = LegalIP(host).test_parameter()  # type:dict

        if data.get('error'):  # 判断结果
            res.code = 500
            res.error = data.get('error')
            # return Response(res.__dict__)
            return HttpResponse(json.dumps(res.__dict__))


        # 判断ip是否存在
        has_ip = models.AnsibleHost.objects.filter(ip=host).first()

        if has_ip:
            res.code = 500
            res.error = "ip已经在数据库中"
            # return Response(res.__dict__)
            return HttpResponse(json.dumps(res.__dict__))

        port = self.request.data.get('port')
        version = self.request.data.get('version')  # 表单数据,centos版本
        user = self.request.data.get('user')
        pwd = self.request.data.get('pwd')

        result = LoginLinux(host,port,version,user,pwd).copy_id()
        # print(result)
        if result.get("error"):
            res.code = 500
            res.error = result.get("error")
            return HttpResponse(json.dumps(res.__dict__))


        # 插入数据库中
        try:
            obj = models.AnsibleHost.objects.create(ip=host,group_id=pk)
            # print(obj)
            # print(host,pk)
            if obj:
                res.url = "/web/ansible/list/"
            else:
                res.code = 500
                res.error = "插入记录失败"
                return HttpResponse(json.dumps(res.__dict__))

            # return HttpResponse(json.dumps(res.__dict__))

        except Exception as e:
            print(e)
            res.code = 500
            res.error = "插入记录异常"
            return HttpResponse(json.dumps(res.__dict__))

        # 写入到配置文件中
        queryset = models.AnsibleGroup.objects.all()
        result = FM(queryset).write()  # type:dict
        # print(result)
        if result.get("error"):
            res.code = 500
            res.error = result.get("error")
            return HttpResponse(json.dumps(res.__dict__))


        # 执行setup模块,收集主机硬件信息
        data = exec_ansible(module='setup', args='', host=host)
        # 判断执行结果
        if not data:
            res.code = 500
            res.error = "执行错误"
            return HttpResponse(json.dumps(res.__dict__))

        # 将执行结果进行筛选,提取有效数据
        data = extract(host, data).get_info()
        # print(data)
        try:
            with transaction.atomic():  # 使用事务
                # 插入一条记录
                # 主机
                host = models.Host.objects.create(hostname=data['hostname'], cpu=data['cpu'], memory=data['memory'],
                                                  os=data['os'],host=obj)
                # host = models.Host.objects.filter(id=1).first()
                # print(host)

                # 主机详情
                models.HostInfo.objects.create(cpu_info=data['cpu_info'], kernel=data['kernel'], sn=data['sn'],
                                               os_version=data['os_version'], host=host)

                # 磁盘
                for i in data['disk']:
                    models.Disk.objects.create(device_name=i['device_name'], disk_type=i['disk_type'],
                                               disk_size=i['disk_size'], host=host)

                # 网卡信息
                for i in data['network_card']:
                    models.Network.objects.create(network_name=i['network_name'], ipaddr=i['ipaddr'],
                                                  netmask=i['netmask'],
                                                  network=i['network'], mac_addr=i['mac_addr'],
                                                  bandwidth=i['bandwidth'],
                                                  active=i['active'], host=host)

                res.url = '/web/ansible/list'
                return HttpResponse(json.dumps(res.__dict__))

        except Exception as e:
            print(e)
            res.code = 500
            res.error = "插入记录失败"
            return HttpResponse(json.dumps(res.__dict__))


    def delete(self, request,pk, *args, **kwargs):
        """
        删除ansible组
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        res = BaseResponse()
        try:
            ret = models.AnsibleGroup.objects.filter(id=pk).delete()
            # print(ret)
            if not ret[0]:
                res.code = 500
                res.error = "删除记录失败"

            # 写入到配置文件中
            queryset = models.AnsibleGroup.objects.all()
            result = FM(queryset).write()  # type:dict
            # print(result)
            if result.get("error"):
                res.code = 500
                res.error = result.get("error")
                return HttpResponse(json.dumps(res.__dict__))

            return HttpResponse(json.dumps(res.__dict__))

        except Exception as e:
            print(e)
            res.code = 500
            res.error = "删除记录异常"
            return HttpResponse(json.dumps(res.__dict__))