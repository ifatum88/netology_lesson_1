from django.contrib import admin

from advertisements.models import Advertisement, Favorits

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'creator', 'created_at']
    list_filter = ['status', 'creator']
    
@admin.register(Favorits)
class FavoritsAdmin(admin.ModelAdmin):
    list_display = ['id', 'advertisement','creator', 'created_at']
    list_filter = ['advertisement', 'creator']