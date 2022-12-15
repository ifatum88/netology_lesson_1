from django.urls import path
from measurement.views import SensorsView, MeasurementView

urlpatterns = [
    # Датчики
    path('sensors/', SensorsView.as_view(), name="sensors_list"),
    path('sensors/<int:pk>/', SensorsView.as_view(), name="sensor_post_or_patch"),
    
    # Измерения
    path('measurements/', MeasurementView.as_view(), name="measurements_list",),
    path('measurements/<int:pk>/', MeasurementView.as_view(), name="measurement_photo_upload"),
    
]
