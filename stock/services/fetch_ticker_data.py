from django.db import models
from stock.models import Ticker


# Query to get all objects of Ticker model
def fetch_ticker_data(market=None,limit=None):
    tickers = Ticker.objects.all().filter(listing=True)
    if(limit):
        tickers=tickers[:limit]
    if market:
        tickers=tickers.filter(market=market)
    return tickers
