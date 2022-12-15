from django.http import Http404
from PIL import Image

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.parsers import FileUploadParser

from .models import Measurement, Sensor
from .serializers import SensorSerializer, MeasurementSerializer, SensorMeasurementSerializer

def drf_check(serializer, true_status) -> Response:
    
    """
    Функция для обработки однотипных проверок DRF
    
    Returns: Response
    """
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=true_status)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def obj_validator(obj_, pk):
    try:
        return obj_.objects.get(pk=pk)
    except:
        raise ParseError("Object not found")
    
def pk_handler(obj_, pk):
    if pk:
        return obj_validator(obj_, pk)
    else:
        return obj_.objects.all()
    
# Датчики
class SensorsView(APIView):
        
    def sensor_serializer(self, obj_, pk):
        if pk:
            return SensorMeasurementSerializer(obj_)
        else:
            return SensorSerializer(obj_, many=True)
    
    def get(self, request, pk=None):
        
        sensors = pk_handler(Sensor, pk) 
        
        if sensors is None:
            return Response({'status': f'id={pk} is not found'}, status.HTTP_404_NOT_FOUND)
               
        ser = self.sensor_serializer(sensors, pk)

        return Response(ser.data)
    
    def post(self, request):
        post_data = request.data
        ser = SensorSerializer(data=post_data)
        
        return drf_check(ser, status.HTTP_201_CREATED)
    
    def patch(self, request, pk):
        sensor_obj = obj_validator(Sensor, pk)
        patch_data = request.data
        ser = SensorSerializer(sensor_obj, data=patch_data, partial=True)
        
        return drf_check(ser, status.HTTP_200_OK)
    
# # Измерения
# class MeasurementView(APIView):
#     parser_classes = [FileUploadParser]
    
#     def get(self, request):
#         measurements = Measurement.objects.all()
#         ser = MeasurementSerializer(measurements, many=True)
#         return Response(ser.data)
    
#     def post(self, request):
#         post_data = request.data
#         ser = MeasurementSerializer(data=post_data)
        
#         return drf_check(ser, status.HTTP_201_CREATED)  
    
#     def patch(self, request, pk):
#         measure_obj = obj_validator(Measurement, pk)
#         patch_data = request.data
#         ser = MeasurementSerializer(measure_obj, data=patch_data, partial=True)
        
#         return drf_check(ser, status.HTTP_200_OK)

class MeasurementView(GenericAPIView, 
                      ListModelMixin,
                      CreateModelMixin,
                      UpdateModelMixin):
    
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)