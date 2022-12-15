from .models import Sensor, Measurement

from rest_framework import serializers

from django.forms import fields


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']

class MeasurementSerializer(serializers.ModelSerializer):
    photo = fields.ImageField(allow_empty_file=True)
    class Meta:
        model = Measurement
        fields = ['id', 'sensor', 'temperature', 'date', 'photo']
        
class SensorMeasurementSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']