from rest_framework import serializers

from util.safe_int import safe_cast_int
from .models import Ticker, Price
from datetime import datetime
from pandas import Timestamp


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
    def to_internal_value(self, data):
        # 원본 데이터의 필드 이름을 모델의 필드 이름에 맞게 변환
        internal_data = {
            'ticker': self.context.get('ticker').id,
            'open': safe_cast_int(data.get('Open')),
            'high': safe_cast_int(data.get('High')),
            'low': safe_cast_int(data.get('Low')),
            'close': safe_cast_int(data.get('Close')),
            'volume': safe_cast_int(data.get('Volume')),
            'date': data.get('Date').strftime('%Y-%m-%d'),
            'is_finalized': self.context.get('is_finalized', True)
        }
        return super().to_internal_value(internal_data)

    def create(self, validated_data):
        # 유효성 검증이 완료된 데이터로 Price 객체 생성
        return Price.objects.create(**validated_data)

