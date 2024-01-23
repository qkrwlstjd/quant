from django.http import JsonResponse
from rest_framework import views
from rest_framework.response import Response
from stock.models import Price
from stock.serializers import PriceSerializer
from datetime import datetime, timedelta
import pandas as pd
import talib
from drf_spectacular.utils import extend_schema, OpenApiParameter
import json

class PriceListView(views.APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(name='ticker', type=str, location=OpenApiParameter.QUERY, description='Ticker symbol'),
        ],
    )
    def get(self, request, *args, **kwargs):
        ticker = self.request.query_params.get('ticker')

        # ticker_query 함수에서 데이터 필터링
        queryset = self.ticker_query(ticker)

        # queryset을 DataFrame으로 변환
        df = pd.DataFrame.from_records(queryset.values())
        df['20d_ma'] = talib.SMA(df['close'], timeperiod=20)

        # DataFrame을 JSON 형식으로 변환
        json_data = df.to_json(orient='records')

        # JSON 데이터를 Response 객체로 반환
        return JsonResponse(json.loads(json_data), safe=False)

    def ticker_query(self, ticker):
        today = datetime.now().date()
        three_months_ago = today - timedelta(days=90)

        # 오늘 날짜에 대한 데이터 필터링
        today_queryset = Price.objects.filter(ticker__name=ticker, date=today, is_finalized=False)

        # 과거 3개월치 데이터 필터링
        past_queryset = Price.objects.filter(ticker__name=ticker, date__range=[three_months_ago, today],
                                             is_finalized=True)

        # 두 쿼리셋을 합쳐서 반환
        return today_queryset.union(past_queryset)
