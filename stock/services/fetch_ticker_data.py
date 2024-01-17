from django.db import models
from stock.models import Ticker


# Query to get all objects of Ticker model
def fetch_ticker_data(market=None):
    tickers = Ticker.objects.all()
    if market:
        tickers.filter(market)
    print(tickers.query)
    return tickers
