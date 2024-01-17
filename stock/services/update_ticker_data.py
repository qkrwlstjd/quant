from django.db import models
from stock.models import Ticker
from stock.serializers import TickerSerializer


# Query to get all objects of Ticker model
def update_ticker_data(ticker,listing):
    ticker_serializer = TickerSerializer(data=ticker)
    ticker_serializer.validated_data['listing'] = listing
    if TickerSerializer.is_valid():
        ticker_serializer.save()