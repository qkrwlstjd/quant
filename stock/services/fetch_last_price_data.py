from django.db import models
from stock.models import Price
from datetime import date, timedelta


# Query to get all objects of Ticker model
def fetch_last_date(ticker,is_finalized=True):
    # is_finalized 값에 따라 필터를 적용하고 마지막으로 생성된 1개의 Price 객체를 가져옴
    last_price = Price.objects.filter(ticker=ticker,is_finalized=is_finalized).order_by('-date').first()

    if last_price:
        return last_price.date
    else:
        return None