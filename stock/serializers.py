from rest_framework import serializers
from .models import Ticker, Price

# Ticker 모델에 대한 시리얼라이저
class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticker
        fields = '__all__'  # 모든 필드를 포함

# Price 모델에 대한 시리얼라이저
class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'  # 모든 필드를 포함
