from django.db import models
from stock.models import Ticker


# Query to get all objects of Ticker model
def fetch_ticker_data(code=None, market=None, limit=None):
    tickers = Ticker.objects.all().filter(listing=True)
    if market:
        tickers = tickers.filter(market=market)
    if code:
        tickers = tickers.filter(code=code)
    if limit:
        tickers = tickers[:limit]
    return tickers
