import yfinance as yf

from scripts.external_services.kis_api import KisApi
from stock.services.fetch_ticker_data import fetch_ticker_data


def fetch_ticker_info():
    tickers = fetch_ticker_data()
    kis_api = KisApi(env='prod')
    kis_api.token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjQxM2JhNzU1LThhYjItNGU5Yi1iZjUxLWZhZjllYzgzMzExMyIsImlzcyI6InVub2d3IiwiZXhwIjoxNzA2OTAyOTgzLCJpYXQiOjE3MDY4MTY1ODMsImp0aSI6IlBTbXQ4ck4xQld5c3JsSUVZSWRJZ0M0a2RBZWJaWHRjdHBkaiJ9.4hL6zzm8BZ5KJLEZiriCnexujfQXUfm7DH03GuczgvwmSOzH3vp5AaSmlg2E8odbEb0ys73hTdYiMDMTrD01aw'

    for ticker in tickers:
        stock=kis_api.get_stock_price(ticker.code)
        ticker.shares = float(stock['lstn_stcn'])
        ticker.save()
        # save_ticker_info(ticker)
