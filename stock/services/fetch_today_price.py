from stock.services.fetch_unfinalized_price_data import fetch_unfinalized_price_data
from datetime import datetime


def fetch_today_price(ticker, market):
    today = datetime.today().strftime('%Y-%m-%d')
    return fetch_unfinalized_price_data(ticker, market, today)
