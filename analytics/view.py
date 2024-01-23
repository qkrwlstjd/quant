from rest_framework import viewsets

from stock.models import Price
from stock.serializers import PriceSerializer
from .models import Indicators
from .serializers import MyModelSerializer
from datetime import datetime, timedelta
import pandas as pd
from rest_framework.response import Response
import talib


class IndicatorsViewSet(viewsets.ModelViewSet):
    queryset = Indicators.objects.all()
    serializer_class = MyModelSerializer


class PriceViewSet(viewsets.ReadOnlyModelViewSet):  # ReadOnlyModelViewSet 사용
    serializer_class = PriceSerializer

    def get_queryset(self):
        today = datetime.now().date()
        three_months_ago = today - timedelta(days=90)

        # 오늘 날짜에 대한 데이터 필터링
        today_queryset = Price.objects.filter(date=today, is_finalized=False)

        # 과거 3개월치 데이터 필터링
        past_queryset = Price.objects.filter(date__range=[three_months_ago, today], is_finalized=True)

        # 두 쿼리셋을 합쳐서 반환
        return today_queryset.union(past_queryset)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # queryset을 DataFrame으로 변환
        df = pd.DataFrame.from_records(queryset.values())
        df['20d_ma'] = talib.SMA(df['Close'], timeperiod=20)

        # DataFrame을 JSON 형식으로 변환
        json_data = df.to_json(orient='records')

        # JSON 데이터를 Response 객체로 반환
        return Response(json_data)
