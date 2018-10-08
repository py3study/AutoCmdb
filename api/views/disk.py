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


class DiskView(ViewSetMixin, APIView):
    def get_msg(self, request,pk, *args, **kwargs):
        """
        磁盘信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        queryset = models.Disk.objects.filter(host_id=pk)
        # print(queryset.values())
        serializer_class = DiskSerializer
        data = SerializedData(request, queryset, serializer_class).get_data()
        # print(data)
        # if not data:

        return HttpResponse(json.dumps(data))
        # return Response(data)