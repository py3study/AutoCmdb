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

class MemoryView(ViewSetMixin, APIView):
    def add(self, request, *args, **kwargs):
        # res = {"code":0}
        res = BaseResponse()
        # print(self.request.data)
        host = self.request.data.get('ip')  # 表单数据
        # print(host)
        # 检测ip是否合格
        data = LegalIP(host).test_parameter()  # type:dict

        if data.get('error'):  # 判断结果
            res.code = 500
            res.error = data.get('error')
            # return Response(res.__dict__)
            return HttpResponse(json.dumps(res.__dict__))

        # 接收监控数据

        # cpu = self.request.data.get('cpu')
        cur_mem = self.request.data.get('cur_mem')
        mem_rate = self.request.data.get('mem_rate')
        mem_all = self.request.data.get('mem_all')
        create_time = self.request.data.get('create_time')
        time_stamp = self.request.data.get('time_stamp')

        # 存入数据库中
        try:
            with transaction.atomic():  # 使用事务
                host = models.Network.objects.filter(ipaddr=host).values("host_id").first()
                if host:
                    # 获取主机id
                    host_id = host.get("host_id")
                    # 内存监控表插入一条记录
                    models.MemoryMonit.objects.create(cur_mem=cur_mem,mem_rate=mem_rate,mem_all=mem_all,create_time=create_time,time_stamp=time_stamp,host_id=host_id)
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
        queryset = models.MemoryMonit.objects.filter(host_id=pk)
        data = []  # 创建一个空列表
        for i in queryset:  # 遍历，拼横纵坐标
            # 横坐标为时间戳,纵坐标为cpu使用率。注意，必须转换类型，否则数据不对。
            data.append([int(i.time_stamp), float('%.2f' % i.mem_rate)])

        # print(data)

        isdict = json.dumps(data)  # json序列化列表
        return HttpResponse(isdict, content_type="application/json")  # 执行类型为json