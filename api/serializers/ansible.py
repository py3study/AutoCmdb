from rest_framework import serializers
from repository import models

class AnsibleSerializer(serializers.ModelSerializer):
    host = serializers.SerializerMethodField()

    class Meta:
        model = models.AnsibleGroup
        # fields = '__all__'
        fields = ['id', 'name', 'host']

    def get_host(self, row):
        host_list = row.ansiblehost_set.all()
        return [{'ip': item.ip} for item in host_list]