from rest_framework import serializers
from repository import models


class HostInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HostInfo
        fields = '__all__'
        # fields = ['cpu_info']