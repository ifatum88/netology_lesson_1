from django.contrib import admin
from phones.models import Phone
# Register your models here.

@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['id','name', 'release_date', 'slug', 'price']
    list_filter = ['name', 'release_date']