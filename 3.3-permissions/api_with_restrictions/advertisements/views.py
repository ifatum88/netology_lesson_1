from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from django.shortcuts import redirect

from django_filters.rest_framework import DjangoFilterBackend

from advertisements.serializers import AdvertisementSerializer
from advertisements.models import Advertisement
from advertisements.permissions import IsOwner
from advertisements.filters import AdvertisementFilter

def main_page(request):
    return redirect('api/')
    

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description']
    # filterset_fields = ['status', 'created_at']
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    
    def get_permissions(self):
        # Тут переписано через стандартный метод get_permissions()
        # и добавлена проверка аутентицикации для NO SAFE методов
        if self.action not in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated] + self.permission_classes 
        
        return super().get_permissions()
    
    def get_queryset(self):
        """ Кастомная реализация фильтрации """
        
        filter_ = {
            'status': self.request.GET.get('status'),
            'created_at_after': self.request.GET.get('created_at_after'),
            'created_at_before': self.request.GET.get('created_at_before'), 
            'created_at': self.request.GET.get('created_at'),
        }

        return AdvertisementFilter(filter_,super().get_queryset()).qs