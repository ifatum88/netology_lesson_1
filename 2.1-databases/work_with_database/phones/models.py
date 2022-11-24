from django.db import models


class Phone(models.Model):
    name = models.CharField(max_length=50,default=None)
    price = models.FloatField(default=0.00)
    image = models.URLField(blank=True)
    release_date = models.DateField(default="1900-01-01")
    lte_exists  = models.BooleanField(default=False)
    slug = models.SlugField(max_length=50)
    
    def __str__(self) -> str:
        return self.slug