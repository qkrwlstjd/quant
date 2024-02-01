import yfinance as yf

from scripts.external_services.kis_api import KisApi
from stock.services.fetch_ticker_data import fetch_ticker_data


def fetch_ticker_info():
    tickers = fetch_ticker_data()
    kis_api = KisApi(env='prod')

    for ticker in tickers:
        stock = kis_api.get_stock_price(ticker.code)
        ticker.shares = float(stock['lstn_stcn'])
        if stock['lstn_stcn'] == '0':
            print(ticker.code,stock)
        ticker.save()
        # save_ticker_info(ticker)
