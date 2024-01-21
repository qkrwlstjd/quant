from stock.serializers import TickerSerializer
from django.forms.models import model_to_dict


def update_ticker_data(ticker, listing):
    ticker = model_to_dict(ticker)
    ticker['listing'] = listing
    ticker_serializer = TickerSerializer(data=ticker)
    if ticker_serializer.is_valid():
        ticker_serializer.save()
