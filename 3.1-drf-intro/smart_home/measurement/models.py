from django.db import models

from datetime import datetime

class Sensor(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    description = models.CharField(max_length=100, verbose_name='Описание')
    
    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_sensor_name"
            )
        ]

    def __str__(self):
        return self.name
    
class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="measurements")
    temperature = models.FloatField(verbose_name='Температура')
    date = models.DateTimeField(verbose_name='Дата измерения', default=datetime.now)
    photo = models.ImageField(verbose_name="Фотография", blank=True)
    
    class Meta:
        verbose_name = 'Измерение температуры'
        verbose_name_plural = 'Измерения температуры'
        