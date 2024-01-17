import yfinance as yf
from rest_framework import serializers


# Define a function to get stock price from yfinance
def fetch_unfinalized_price_data(ticker, market, start, end):
    ticker = ticker.zfill(6)
    market_type = market.split(" ")[0]
    if market_type == "KOSPI":
        ticker_symbol = ticker + ".KS"
    elif market_type == "KOSDAQ":
        ticker_symbol = ticker + ".KQ"
    elif market_type == "KONEX":
        ticker_symbol = ticker + ".KN"
    else:
        print(f'Unknown market type: {market_type}. Skipping {ticker}.')
        return []

    stock_data = yf.Ticker(ticker_symbol)

    # 사용자가 지정한 시작 날짜부터 현재까지의 일별 주식 데이터를 가져옴
    data = stock_data.history(start=start, end=end)

    # 날짜 인덱스를 컬럼으로 변환
    data.reset_index(inplace=True)

    # 데이터를 딕셔너리 형태로 변환
    data_dict = data.to_dict('records')
    return data_dict
