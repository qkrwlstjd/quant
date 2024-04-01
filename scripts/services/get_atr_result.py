import talib

from scripts.services.get_buyline import get_buy_condition
from scripts.services.get_price import get_price_list
from scripts.services.process_and_thread import ProcessAndThread
from stock.models import AtrResult, Price
from django.db.models import F, FloatField
from django.db.models.functions import Cast
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


def get_atr_result(code=None, date=None):
    query = AtrResult.objects.all().select_related('ticker', 'price').annotate(liq_line=F('price__open'))
    if code:
        query = query.filter(code=code)
    if date:
        query = query.filter(price__date__lte=date)

    return query


def calc():
    # 시작일 설정 (2020년 1월 1일)
    date = datetime(2020, 3, 29)

    # 현재 날짜 설정
    current_date = datetime.now()

    # 1일씩 증가하면서 현재 날짜까지 반복
    while date <= current_date:
        atr_list = list(get_atr_result(date=date).filter(sell_price__isnull=True).values())
        if (len(atr_list) > 0):
            print(date, len(atr_list))
            ProcessAndThread(func=pp, item=atr_list, args={'date': date}).process()

        date += timedelta(days=1)  # 다음 날짜로 이동


def pp(atr, obj):
    price_list = get_price_list(code=atr["ticker_id"], date=obj["date"])
    df = get_ma(price_list)
    last_row = df.iloc[-1:].copy()
    last_row_json = last_row.to_dict(orient='records')[0]

    if (not atr["sell_price_id"]) and (
            last_row_json["MA_20"] > np.maximum(last_row_json["open"], last_row_json["close"]) or
            last_row_json["MA_60"] > np.maximum(last_row_json["open"], last_row_json["close"]) or
            atr["liq_line"] > last_row_json["close"]
    ):
        atr_obj = AtrResult.objects.get(id=atr["id"])
        atr_obj.sell_price_id = last_row_json["id"]
        atr_obj.save()
    elif (not atr["buy_price_id"]) and \
            (last_row_json["MA_20"] > last_row_json["low"]) or \
            (last_row_json["MA_60"] > last_row_json["low"]):
        atr_obj = AtrResult.objects.get(id=atr["id"])
        atr_obj.buy_price_id = last_row_json["id"]
        atr_obj.save()


def get_ma(price_list):
    df = pd.DataFrame.from_records(price_list)
    df['MA_5'] = talib.MA(df['close'], timeperiod=5)
    df['MA_20'] = talib.MA(df['close'], timeperiod=20)
    df['MA_60'] = talib.MA(df['close'], timeperiod=60)
    return df
