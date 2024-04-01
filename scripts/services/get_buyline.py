from itertools import zip_longest

import pandas as pd
import talib
import numpy as np
from multiprocessing import Pool
from stock.models import Price, AtrResult
from stock.services.fetch_ticker_data import fetch_ticker_data
import pandas as pd
import sys
from scripts.services.get_price import get_price, get_price_list
from util.cross import cross
from util.safe_int import safe_cast_int


# price_df 데이터프레임을 전부 출력합니다.


def get_all_ticker_price(code=None, limit=60, _type='mix', recent=False, test=False):
    tickers = list(fetch_ticker_data(code=code).values())
    for ticker in tickers:
        price_list = get_price_list(ticker['code'], recent)
        price_df = get_buy_condition(price_list, limit, _type)
        if test:
            price_df = get_buy_additional_condition(price_df)
            print(price_df)
        else:
            save_atr_result(price_df)


def save_atr_result(price_df):
    rows_to_save_0 = price_df[price_df['BUY_CONDITION'].shift(-1).fillna(False)].copy().to_dict(orient='records')
    rows_to_save_1 = price_df[price_df['BUY_CONDITION']].copy().to_dict(orient='records')
    rows_to_save_2 = price_df[price_df['BUY_CONDITION'].shift().fillna(False)].copy().to_dict(orient='records')
    objects_to_create = []
    for row_data0, row_data1, row_data2 in zip_longest(rows_to_save_0, rows_to_save_1, rows_to_save_2, fillvalue=None):
        if row_data0 is None or row_data1 is None or row_data2 is None:
            continue
        atr_result = AtrResult(
            ticker_id=row_data1['ticker_id'],
            price_id=int(row_data1['id']),
            atr_line=row_data1['BUY_LINE'],
            ma5=row_data1['MA_5'],
            ma20=row_data1['MA_20'],
            ma60=row_data1['MA_60'],
            ma5_cross=row_data1["MA_5_CROSS"],
            ma20_cross=row_data1["MA_20_CROSS"],
            ma60_cross=row_data1["MA_60_CROSS"],
            prev_price_id=int(row_data0['id']),
            next_price_id=int(row_data2['id']),
        )
        objects_to_create.append(atr_result)
    try:
        AtrResult.objects.bulk_create(objects_to_create)
    except Exception as e:
        print(objects_to_create)
        for o in objects_to_create:
            try:
                o.save()
            except Exception as e2:
                print(o)
                print(e2)
        print(e)


def get_buy_condition(price_list, limit=60, _type='mix'):
    # queryset을 DataFrame으로 변환
    df = pd.DataFrame.from_records(price_list)
    df['date'] = pd.to_datetime(df['date'])
    df['DATE'] = df['date'].dt.strftime('%Y%m%d')

    df['MA_5'] = talib.MA(df['close'], timeperiod=5)
    df['MA_20'] = talib.MA(df['close'], timeperiod=20)
    df['MA_60'] = talib.MA(df['close'], timeperiod=60)

    df['TR'] = talib.TRANGE(df['high'], df['low'], df['close'])
    df['ATR'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=limit)
    df['NOISE'] = 1 - (df['open'] - df['close']).abs() / (df['high'] - df['low'])
    df['NOISE'] = df['NOISE'].fillna(0).clip(0, 1)
    df['NOISE_SMA'] = talib.SMA(df['NOISE'], timeperiod=limit)
    if _type == 'mix':
        df['BUY_LINE'] = df['open'] + np.maximum(df['TR'] * df['NOISE_SMA'], df['ATR'])
    elif _type == 'atr':
        df['BUY_LINE'] = df['open'] + df['ATR']
    elif _type == 'noise':
        df['BUY_LINE'] = df['open'] + df['TR'] * df['NOISE_SMA']
    df['BUY_CONDITION'] = df['close'] > df['BUY_LINE']
    df["MA_5_CROSS"], _ = cross(df['close'], df['MA_5'])
    df["MA_20_CROSS"], _ = cross(df['close'], df['MA_20'])
    df["MA_60_CROSS"], _ = cross(df['close'], df['MA_60'])

    # df["CROSS_OVER"] = df["MA_5_CROSS"] & df["MA_20_CROSS"] & df["MA_60_CROSS"]
    ########################

    ########################
    # # DataFrame을 JSON 형식으로 변환
    # json_data = df.to_json(orient='records')
    #
    # # JSON 데이터를 Response 객체로 반환
    # return json_data
    return df


PRICE_CHANGE_POINT = {
  "1": 0.05012902,
  "2": 0.06455308,
  "3": 0.17872773,
  "4": 0.24278761,
  "5": 0.36905651,
  "6": 0.37141226,
  "7": 0.34134222,
  "8": 0.36641654,
  "9": 0.27454213,
  "10": 0.27493022,
  "11": 0.42986565,
  "12": 0.34083624,
  "13": 0.14641661,
  "14": 0.2405455,
  "15": 0.55827352,
  "16": 0.3896218,
  "17": 0.53881151,
  "18": 0.34709375,
  "19": 0.13386004,
  "20": 0.45032842,
  "21": 0.26600541,
}

def get_buy_additional_condition(df):
    #####돌파 9%이내 조건#####
    df["PREV_CLOSE"] = df['close'].shift().fillna(0)
    df["PRICE_CHANGE"] = np.where(df["PREV_CLOSE"] != 0, (df["close"] - df["PREV_CLOSE"]) / df["PREV_CLOSE"] * 100,
                                  np.nan)
    df["PRICE_CHANGE_POINT"] = df["PRICE_CHANGE"].apply(lambda x: PRICE_CHANGE_POINT.get(str(safe_cast_int(x)), -1))
    df['BUY_CONDITION'] = df['BUY_CONDITION'] & (df["PRICE_CHANGE"] < 22) & (df["PRICE_CHANGE"] > 5)
    return df
