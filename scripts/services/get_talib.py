import talib

from stock.models import Price
import pandas as pd
from scripts.services.get_price import get_price
import json


def get_talib():
    price_list = get_price('101680')[:60]

    # queryset을 DataFrame으로 변환
    df = pd.DataFrame.from_records(price_list)

    df['corr_STOCHRSI_K'],df['corr_STOCHRSI_D'] = talib.STOCHRSI(df['close']) # K=10
    df['corr_STOCHRSI_SK'], df['corr_STOCHRSI_SD'] = talib.STOCH(high=df['high'], low=df['low'],close=df['close'])
    df['corr_STOCHRSI_FK'], df['corr_STOCHRSI_FD'] = talib.STOCHF(high=df['high'], low=df['low'],close=df['close'])

    df_json = df.to_json(orient='records', date_format='iso')
    pretty_printed_json = json.dumps(df_json, indent=4)
    print(pretty_printed_json)
    print(df_json)
