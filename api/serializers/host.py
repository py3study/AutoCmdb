from rest_framework import serializers
from repository import models


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Host
        fields = '__all__'


class HostListSerializer(serializers.ModelSerializer):
    ipaddr = serializers.SerializerMethodField()

    class Meta:
        model = models.Host
        # fields = '__all__'
        fields = ['id', 'hostname', 'cpu', 'memory', 'os', 'status', 'ipaddr']

    def get_ipaddr(self, row):
        ipaddr_list = row.network_set.all()
        return [{'ipaddr': item.ipaddr} for item in ipaddr_list]
