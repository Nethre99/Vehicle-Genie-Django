from rest_framework import serializers
from . import models
from .models import vehicles


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = vehicles
        fields = '__all__'


class UserVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserVehicle
        fields = '__all__'