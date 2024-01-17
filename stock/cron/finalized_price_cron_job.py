from django_cron import CronJobBase

from stock.services.fetch_last_price_data import fetch_last_date
from stock.services.fetch_ticker_data import fetch_ticker_data
from stock.services.fetch_finalized_price_data import fetch_finalized_price_data
from stock.services.fetch_unfinalized_price_data import fetch_unfinalized_price_data
from stock.services.update_ticker_data import update_ticker_data
from stock.serializers import PriceSerializer, TickerSerializer


class PriceFinalizationCronJob(CronJobBase):
    """This job handles the finalization of prices"""
    schedule = "0 0 1 1 *"
    code = 'finalized_price_cron_job'  # 크론 작업의 코드 식별자

    def do(self):
        tickers = fetch_ticker_data()
        for ticker in tickers:
            fetch_last_ticker_data = fetch_last_date(ticker)
            data = fetch_finalized_price_data(ticker.code, ticker.market, fetch_last_ticker_data if fetch_last_ticker_data else "2000-01-01")
            if data is [] and fetch_last_ticker_data is None:
                update_ticker_data(ticker, False)
            else:
                if fetch_last_ticker_data is not None and str(data[-1]['Date'].strftime('%Y-%m-%d')) == str(fetch_last_ticker_data):
                    print(ticker.name,fetch_last_ticker_data)
                    continue
                price_serializer = PriceSerializer(data=data, many=True,
                                                   context={'ticker': ticker, 'is_finalized': True})
                if price_serializer.is_valid():
                    price_serializer.save()
                else:
                    print(price_serializer.errors)
