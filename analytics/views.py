from itertools import chain

import numpy as np
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
from analytics.utils.cross import cross


class PriceListView(views.APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        parameters=[
            OpenApiParameter(name='code', type=str, location=OpenApiParameter.QUERY, description='code'),
            OpenApiParameter(name='date', type=str, location=OpenApiParameter.QUERY, description='date'),

        ],
    )
    def get(self, request, *args, **kwargs):
        code = self.request.query_params.get('code')
        date = self.request.query_params.get('date', datetime.now().strftime('%Y%m%d'))
        json_data = self.get_buy_condition(code, date, limit=20)

        # JSON 데이터를 Response 객체로 반환
        return JsonResponse(json.loads(json_data), safe=False)

    def get_buy_condition(self, code, date, limit):f['TR'] = talib.TRANGE(df['high'], df['low'], df['close'])
        df['ATR'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=limit)
        df['NOISE'] = 1 - (df['open'] - df['close']).abs() / (df['high'] - df['low'])
        df['NOISE_SMA'] = talib.SMA(df['NOISE'], limit)
        df['BUY_LINE'] =
        price_list = self.get_query(code, date, limit)

        # queryset을 DataFrame으로 변환
        df = pd.DataFrame.from_records(price_list)
        df['date'] = pd.to_datetime(df['date'])
        df['DATE'] = df['date'].dt.strftime('%Y%m%d')

        ddf['open'] + np.maximum(df['TR'] * df['NOISE_SMA'], df['ATR'])
        df['BUY_CONDITION'] = df['close'] > df['BUY_LINE']
        df['PROFIT'] = np.where(df['BUY_CONDITION'].shift(1),
                                (((df['open'] - df['close'].shift(1)) / df['close'].shift(1) * 100) - 0.1), 0)
        df['CUMULATIVE_PROFIT'] = df['PROFIT'].cumsum()
        df['CUMULATIVE_PROFIT_SUM'] = df['BUY_CONDITION'].cumsum()

        # DataFrame을 JSON 형식으로 변환
        json_data = df.to_json(orient='records')

        # JSON 데이터를 Response 객체로 반환
        return json_data

    def get_query(self, code, date, limit):
        today = datetime.strptime(date, '%Y%m%d').date()

        # date보다 낮은 날짜의 데이터 필터링 및 내림차순 정렬
        price_list = Price.objects.filter(ticker__code=code, date__lte=today, is_finalized=True) \
                         .order_by('-date').values()[:limit+240]  # 최대 14개 반환
        price_list = price_list[::-1]

        # 결과 반환
        return price_list
