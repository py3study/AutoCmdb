from rest_framework import serializers
from repository import models


class DiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Disk
        fields = '__all__'