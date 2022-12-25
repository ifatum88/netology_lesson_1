from django.contrib.auth.models import User
from django.conf import settings

from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices, Favorits


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)
        
    def create(self, validated_data):
        return super().create(validated_data)

# Сериализатор для избранного
class FavoritsSerializer(serializers.ModelSerializer):
    
    creator = UserSerializer(read_only=True)
    
    class Meta:
        model = Favorits
        fields = ('advertisement', 'creator')
        read_only_fields = ['creator']
        
    
class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at')
        read_only_fields = ['creator']

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        
        creator = self.context["request"].user
        validated_data["creator"] = creator
        adv_count_for_user = Advertisement.objects.filter(creator=creator,
                                                          status=AdvertisementStatusChoices.OPEN).count()

        if adv_count_for_user < settings.MAX_ADV_COUNT:
            return super().create(validated_data)
        else:
            raise serializers.ValidationError("Max adv count = {}. Your OPEN adv count = {}".format( 
                                              settings.MAX_ADV_COUNT,
                                              adv_count_for_user))