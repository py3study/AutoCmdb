from rest_framework import serializers
from repository import models


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Network
        fields = '__all__'