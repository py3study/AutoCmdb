from rest_framework.response import Response
from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from repository import models
from api.utils.response import BaseResponse


from api.serializers.disk import DiskSerializer
from api.utils.serialization_general import SerializedData
from api.utils.auth import Authentication
import json

from api.utils.ansible.check_ip import LegalIP
from django.db import transaction

class CpuView(ViewSetMixin, APIView):
    def add(self, request, *args, **kwargs):  # 入库
        # res = {"code":0}
        res = BaseResponse()

        host = self.request.data.get('ip')  # 表单数据
        # 检测ip是否合格
        data = LegalIP(host).test_parameter()  # type:dict

        if data.get('error'):  # 判断结果
            res.code = 500
            res.error = data.get('error')
            return HttpResponse(json.dumps(res.__dict__))

        # 接收监控数据
        cpu = self.request.data.get('cpu')
        create_time = self.request.data.get('create_time')
        time_stamp = self.request.data.get('time_stamp')

        # 存入数据库中
        try:
            with transaction.atomic():  # 使用事务
                # 查询网卡ip,并查询出对应host表的id
                host = models.Network.objects.filter(ipaddr=host).values("host_id").first()
                if host:
                    # 获取主机id
                    host_id = host.get("host_id")
                    # CPU监控表中插入一条记录
                    models.CpuMonit.objects.create(cpu=cpu,create_time=create_time,time_stamp=time_stamp,host_id=host_id)
                    return HttpResponse(json.dumps(res.__dict__))
                else:
                    res.code = 500
                    res.error = "数据库找不到此ip"
                    return HttpResponse(json.dumps(res.__dict__))

        except Exception as e:
            print(e)
            res.code = 500
            res.error = "插入记录失败"
            return HttpResponse(json.dumps(res.__dict__))

    def chart_json(self, request,pk, *args, **kwargs):  # 图表数据
        # 读取表所有记录
        queryset = models.CpuMonit.objects.filter(host_id=pk)
        data = []  # 创建一个空列表
        for i in queryset:  # 遍历，拼横纵坐标
            # 横坐标为时间戳,纵坐标为cpu使用率。注意，必须转换类型，否则数据不对。
            data.append([int(i.time_stamp), float('%.2f' % i.cpu)])

        # print(data)

        isdict = json.dumps(data)  # json序列化列表
        return HttpResponse(isdict, content_type="application/json")  # 执行类型为json