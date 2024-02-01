from itertools import zip_longest

import pandas as pd
import talib
import numpy as np
from multiprocessing import Pool
from stock.models import Price, AtrResult
from stock.services.fetch_ticker_data import fetch_ticker_data


def get_all_ticker_price(limit):
    tickers = list(fetch_ticker_data().values())
    for ticker in tickers:
        price_df = get_buy_condition(ticker, limit)
        buy_condition_true_rows = price_df[price_df['BUY_CONDITION']]
        buy_condition_next_rows = price_df[price_df['BUY_CONDITION'].shift().fillna(False)]

        save_atr_result(buy_condition_true_rows, buy_condition_next_rows, limit)
    # return results


def save_atr_result(row_1, row_2, comment):
    rows_1_to_save = row_1.to_dict(orient='records')
    rows_2_to_save = row_2.to_dict(orient='records')
    objects_to_create = []
    for row_data1, row_data2 in zip_longest(rows_1_to_save, rows_2_to_save, fillvalue=None):
        if row_data1 is None or row_data2 is None:
            # 한쪽 리스트의 요소가 부족한 경우 처리
            continue
        profit = ((row_data2['open'] - row_data1['close']) / row_data1['close']) * 100
        if profit >= 30 or profit <= -30:
            continue
        atr_result = AtrResult(
            ticker_id=row_data1['ticker_id'],
            price_buy_id=int(row_data1['id']),
            price_sell_id=int(row_data2['id']),
            buy_line=row_data1['BUY_LINE'],
            profit=((row_data2['open'] - row_data1['close']) / row_data1['close']) * 100,
            comment=comment
        )
        objects_to_create.append(atr_result)
    AtrResult.objects.bulk_create(objects_to_create)


# for row_data in rows_to_save:
#     # if row_data['BUY_CONDITION']:


def get_buy_condition(ticker, limit):
    price_list = get_price(ticker['code'])

    # queryset을 DataFrame으로 변환
    df = pd.DataFrame.from_records(price_list)
    df['date'] = pd.to_datetime(df['date'])
    df['DATE'] = df['date'].dt.strftime('%Y%m%d')

    df['TR'] = talib.TRANGE(df['high'], df['low'], df['close'])
    df['ATR'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=limit)
    df['NOISE'] = 1 - (df['open'] - df['close']).abs() / (df['high'] - df['low'])
    df['NOISE_SMA'] = talib.SMA(df['NOISE'], limit)
    df['BUY_LINE'] = df['open'] + np.maximum(df['TR'] * df['NOISE_SMA'], df['ATR'])
    df['BUY_CONDITION'] = df['close'] > df['BUY_LINE']
    # # DataFrame을 JSON 형식으로 변환
    # json_data = df.to_json(orient='records')
    #
    # # JSON 데이터를 Response 객체로 반환
    # return json_data
    return df


def get_price(code):
    # date보다 낮은 날짜의 데이터 필터링 및 내림차순 정렬
    price_list = Price.objects.filter(ticker__code=code, is_finalized=True).values()

    # 결과 반환
    return price_list
