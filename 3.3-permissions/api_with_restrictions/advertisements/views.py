from copy import copy

from rest_framework import status

from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from django.shortcuts import redirect

from django_filters.rest_framework import DjangoFilterBackend

from advertisements.serializers import AdvertisementSerializer, FavoritsSerializer
from advertisements.models import Advertisement, Favorits, AdvertisementStatusChoices
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.filters import AdvertisementFilter

def main_page(request):
    return redirect('api/')
    

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description']
    # Доп задание проверки на админа реализовано через проверку IsOwnerOrReadOnly или IsAdminUser
    permission_classes = [IsOwnerOrReadOnly|IsAdminUser]
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        
    def get_permissions(self):
        # Тут переписано через стандартный метод get_permissions()
        # и добавлена проверка аутентицикации
        if self.action in ['create', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated] + self.permission_classes 
        
        return super().get_permissions()
    
    def get_queryset(self):
        """ Кастомная реализация фильтрации """

        # Доп задание DRAFT. Реализовано через модификацию кверисета
        # Проверку прав в таком случае нет смысла делать,
        # так как чужие DRAF увидеть просто невозможно
        if IsAdminUser().has_permission(self.request, self):
            # Если админ - видно все
            queryset = super().get_queryset()
        else:
            # Если не админ - убираем все DRAF
            queryset = super().get_queryset().exclude(status=AdvertisementStatusChoices.DRAFT)
            
            # Если авторизован - добавляем мои DRAFT к queryset
            if IsAuthenticated().has_permission(self.request, self):
                queryset = queryset | super().get_queryset().filter(creator=self.request.user,
                                                                    status=AdvertisementStatusChoices.DRAFT)
        
        # Реализация задания с фильтрами  
        filter_ = {
            'status': self.request.GET.get('status'),
            'created_at_after': self.request.GET.get('created_at_after'),
            'created_at_before': self.request.GET.get('created_at_before'), 
            'created_at': self.request.GET.get('created_at')
        }

        return AdvertisementFilter(filter_, queryset).qs

# Реализация задания с избранным
# Отказался от использования декоратора action
# Так как под каждое действие надо писать свою функцию
# Да и еще описывать ее, что некрасиво. 
class FavoritsView(ModelViewSet):
    
    queryset = Favorits.objects.all()
    serializer_class = FavoritsSerializer
    
    # Перекрыт метод List, чтобы выводить мои избранные объявления
    def list(self, request, *args, **kwargs):
        queryset = Advertisement.objects.all()
        queryset_filtred = queryset.filter(favorits__creator__id=request.user.id)
        serializer = AdvertisementSerializer(queryset_filtred, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Расширен метод create, чтобы отдавать данные по creator и advertisement
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        
    def create(self, request, *args, **kwargs):
        
        request.data['creator'] = request.user
        request.data['advertisement'] = kwargs['pk']
        
        return super().create(request, *args, **kwargs)

    # Перекрыт метод destroy, чтобы удалять нужное объявление
    def destroy(self, request, *args, **kwargs):
        instance = self.queryset.filter(creator=request.user, 
                                        advertisement=kwargs.get('pk'))
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
            