from rest_framework import serializers
from .models import ExchangeInfo, ExchangeDate
from .models import DepositProduct, DepositOption, SavingProduct, SavingOption, Subscribe_Product

class ExchangeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeInfo
        fields = '__all__'  # 모든 필드를 시리얼라이즈

class ExchangeDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeDate
        fields = '__all__'  # 모든 필드를 시리얼라이즈

class DepositOptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = DepositOption
		fields = '__all__'
		read_only_fields = ('product',)
            
class DepositProductSerializer(serializers.ModelSerializer):
	option = DepositOptionSerializer(many=True, read_only=True)

	class Meta:
		model = DepositProduct
		fields = '__all__'  # 모든 필드를 포함합니다.

class SavingOptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = SavingOption
		fields = '__all__'
		read_only_fields = ('product',)

class SavingProductSerializer(serializers.ModelSerializer):
    option = SavingOptionSerializer(many=True, read_only=True)
    class Meta:
        model = SavingProduct
        fields = '__all__'

class SubscribeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe_Product
        fields = '__all__'
