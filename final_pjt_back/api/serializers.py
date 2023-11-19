from rest_framework import serializers
from .models import ExchangeInfo, ExchangeDate
from .models import DepositOptions,DepositProducts

class ExchangeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeInfo
        fields = '__all__'  # 모든 필드를 시리얼라이즈

class ExchangeDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeDate
        fields = '__all__'  # 모든 필드를 시리얼라이즈

class DepositProductsSerializer(serializers.ModelSerializer):
	class Meta:
		model = DepositProducts
		fields = '__all__'

class DepositOptionsserializer(serializers.ModelSerializer):
	class Meta:
		model = DepositOptions
		fields = '__all__'
		read_only_fields = ('product',)
