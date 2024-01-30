from stock.serializers import TickerSerializer
from django.forms.models import model_to_dict


def update_ticker_data(ticker, listing):
    ticker.listing = listing
    ticker.save()
