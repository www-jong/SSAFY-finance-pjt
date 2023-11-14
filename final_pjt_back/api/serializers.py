from rest_framework import serializers
from .models import ExchangeInfo, ExchangeDate

class ExchangeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeInfo
        fields = '__all__'  # 모든 필드를 시리얼라이즈

class ExchangeDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeDate
        fields = '__all__'  # 모든 필드를 시리얼라이즈