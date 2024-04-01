import numpy as np
import talib

from scripts.services.get_pattern_score import get_pattern_score
from stock.models import AtrResult, Price
from django.db.models import Sum, Max, Min, Avg, Count
import pandas as pd
import concurrent.futures
import time
import multiprocessing
from scipy.stats import pointbiserialr, pearsonr, spearmanr
import json
from collections import OrderedDict
import math


def get_buy_info_thread(chunk, max_workers=30):
    atr_results = chunk

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Process AtrResults in parallel
        results = list(executor.map(process_atr, atr_results))

    atr_df = pd.concat(results, ignore_index=True)

    return atr_df


def get_buy_info_process(max_process=4):
    atr_results = list(AtrResult.objects.filter())
    atr_df = pd.DataFrame()  # Initialize an empty DataFrame

    # Split the AtrResults into chunks for parallel processing
    chunk_size = len(atr_results) // max_process
    chunks = [atr_results[i:i + chunk_size] for i in range(0, len(atr_results), chunk_size)]

    with multiprocessing.Pool(processes=max_process) as pool:
        atr_df_chunks = pool.map(get_buy_info_thread, chunks)

    # Combine the results from all chunks
    atr_df = pd.concat(atr_df_chunks, ignore_index=True)

    return atr_df


def calculate_group_with_profit(df,column):
    # 패턴 점수를 정수로 변환
    # NaN 값을 0으로 대체
    df[column].fillna(0, inplace=True)
    df['div'] = df[column]
    # pattern_score의 값을 내림하여 정수로 변환
    df['group'] = np.floor(df['div']).astype(int)

    # pattern_score를 기준으로 그룹화하고 profit의 평균 계산
    grouped = df.groupby('group')['profit'].agg(['mean', 'count'])

    # 결과를 딕셔너리로 변환
    pattern_score_to_avg_profit = grouped.to_dict('index')
    return pattern_score_to_avg_profit

def calculate_correlation(df):
    # Initialize a dictionary to store correlation values
    correlation_dict = {}

    for column in df.columns:
        if column.startswith('corr_'):
            correlation_dict['1' + column + 'c'], correlation_dict['1' + column + 'p'] = pointbiserialr(df[column],
                                                                                                        df['profit'])

            correlation_dict['2' + column + 'c'], correlation_dict['2' + column + 'p'] = pearsonr(df[column],
                                                                                                  df['profit'])

            correlation_dict['3' + column + 'c'], correlation_dict['3' + column + 'p'] = spearmanr(df[column],
                                                                                                   df['profit'])

    return correlation_dict


def process_atr(atr, limit=60):
    prices = (Price.objects.filter(ticker=atr.ticker, date__lte=atr.price_buy.date,is_finalized=True)
              .order_by('-date'))[:limit].values()
    prices_reversed = list(prices)[::-1]
    df = pd.DataFrame.from_records(prices_reversed)
    df['profit'] = atr.profit
    df['buy_line'] = atr.buy_line
    ######################################################################
    # corr_breakout 5 이상
    # df['corr_breakout'] = (df['close'] - atr.buy_line) / df['open'] * 100

    # K 90~100   D 30~100
    # df['corr_STOCHRSI_K'], df['corr_STOCHRSI_D'] = talib.STOCHRSI(df['close'])

    # SK40~109 SD 20~100
    # df['corr_STOCHRSI_SK'], df['corr_STOCHRSI_SD'] = talib.STOCH(high=df['high'], low=df['low'], close=df['close'])

    # FK100  FD 40~109
    # df['corr_STOCHRSI_FK'], df['corr_STOCHRSI_FD'] = talib.STOCHF(high=df['high'], low=df['low'], close=df['close'])
    ######################################################################
    # df['corr_BOP'] = talib.BOP(open=df['open'], high=df['high'], low=df['low'], close=df['close'])
    # df['corr_CCI'] = talib.CCI(high=df['high'], low=df['low'], close=df['close'])
    # df['corr_RSI'] = talib.RSI(df['close'])
    # df['corr_PLUS_DI'] = talib.PLUS_DI(df['high'], df['low'], df['close'],timeperiod=14)
    # df['corr_MINUS_DI'] = talib.MINUS_DI(df['high'], df['low'], df['close'],timeperiod=14)
    # df['corr_DX'] = talib.DX(df['high'], df['low'], df['close'],timeperiod=14)

    ###############################################################

    df['BBANDS_UP'], df['BBANDS_M'], df['BBANDS_DO'] = talib.BBANDS(df['close'], timeperiod=20)
    df['corr_BBANDS_P'] = (df['close'] - df['BBANDS_DO']) / (df['BBANDS_UP'] - df['BBANDS_DO'])
    df['corr_BBANDS_W'] = (df['BBANDS_UP'] - df['BBANDS_DO']) / df['BBANDS_M']

    ###############################################################
    # df['corr_CCI_30_70'] = df['corr_CCI'].between(-100, 100)
    # df['corr_CCI_MINUS'] = df['corr_CCI'].between(-100, -200)
    # df['corr_CCI_PLUS'] = df['corr_CCI'].between(100, 200)
    # df['corr_RSI_30_70'] = df['corr_RSI'].between(30, 70)
    # df['corr_RSI_70_100'] = df['corr_RSI'].between(70, 100)
    # df['corr_RSI_0_40'] = df['corr_RSI'].between(0, 40)
    # df['corr_RSI_40_60'] = df['corr_RSI'].between(40, 60)
    # df['corr_RSI_60_100'] = df['corr_RSI'].between(60, 100)
    # df['corr_RSI_0_20'] = df['corr_RSI'].between(0, 20)
    # df['corr_RSI_20_80'] = df['corr_RSI'].between(20, 80)
    # df['corr_RSI_80_100'] = df['corr_RSI'].between(80, 100)
    # df['corr_ADX'] = talib.ADX(df['high'], df['low'], df['close'],timeperiod=14)
    # df['corr_ADXR'] = talib.ADXR(df['high'], df['low'], df['close'],timeperiod=14)
    # df['corr_APO'] = talib.APO(df['close'])

    last_row = df.iloc[-1:].copy()  # Get the last row
    ######################################################################
    # pattern_score > 3.07 이상
    # last_row['pattern_score'] = get_pattern_score(df)
    ######################################################################
    return last_row


def get_correlation():
    df = get_buy_info_process()
    calculate_group_with_profit_print(df)

def calculate_group_with_profit_print(df):
    for column in df.columns:
        if column.startswith('corr_'):
            print(f"####################{column}#########################")
            correlation = calculate_group_with_profit(df,column)
            pretty_printed_json = json.dumps(correlation, indent=4)
            print(pretty_printed_json)



def sortDict(dict):
    # OrderedDict로 딕셔너리 생성
    ordered_correlation = OrderedDict(dict)

    # 값으로 정렬된 항목 생성
    sorted_items = sorted(ordered_correlation.items(), key=lambda x: x[1])

    # 정렬된 항목으로 새로운 OrderedDict 생성
    sorted_correlation = OrderedDict(sorted_items)
    return sorted_correlation
