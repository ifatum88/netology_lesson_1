from django.urls import path

from advertisements.views import main_page, AdvertisementViewSet, FavoritsView

# Отказ от использования стандартных маршрутов, чтобы сделать красивые
# адреса типа advertisements/favorits/ под все типы запросов

advertisements_list = AdvertisementViewSet.as_view(
    {
        'get': 'list',
        'post': 'create',
    }
)

advertisements_detail = AdvertisementViewSet.as_view(
    {
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy',
    }
)

favorits_list = FavoritsView.as_view(
    {
        'get': 'list',
    } 
)

favorits_detail = FavoritsView.as_view(
    {
        'post': 'create',
        'delete': 'destroy',
    }
)

urlpatterns = [
    path('advertisements/', advertisements_list, name="advertisements_list"),
    path('advertisements/<int:pk>/', advertisements_detail, name="advertisements_detail"),
    
    path('advertisements/favorits/', favorits_list, name="favorits_list"),
    path('advertisements/<int:pk>/favorits/', favorits_detail, name="favorits_create"),
]