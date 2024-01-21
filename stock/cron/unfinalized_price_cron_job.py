from django_cron import CronJobBase, Schedule

from stock.services.fetch_last_price_data import fetch_last_date
from stock.services.fetch_ticker_data import fetch_ticker_data
from stock.services.fetch_finalized_price_data import fetch_finalized_price_data
from stock.services.fetch_unfinalized_price_data import fetch_unfinalized_price_data
from stock.services.save_price_data import save_price_data
from stock.services.update_ticker_data import update_ticker_data
from stock.serializers import PriceSerializer, TickerSerializer
from datetime import datetime, timedelta

class PriceUnfinalizationCronJob(CronJobBase):
    """This job handles the unfinalization of prices"""
    schedule = Schedule(run_at_times=['17:19'])
    code = 'unfinalized_price_cron_job'  # 크론 작업의 코드 식별자

    def do(self):
        tickers = fetch_ticker_data()
        for ticker in tickers:
            last_ticker_data = fetch_last_date(ticker,is_finalized=False)

            today = datetime.now()
            sixty_days_ago = today - timedelta(days=59)
            formatted_sixty_days_ago = sixty_days_ago.strftime('%Y-%m-%d')
            default_date = formatted_sixty_days_ago
            data = fetch_unfinalized_price_data(ticker.code, ticker.market,
                                              last_ticker_data if last_ticker_data else default_date)
            try:
                if data == [] and last_ticker_data is None:
                    raise Exception("Not data and last ticker is not")
                if last_ticker_data is not None and str(data[-1]['Date'].strftime('%Y-%m-%d')) == str(last_ticker_data):
                    print(ticker.name,data[-1]['Date'].strftime('%Y-%m-%d'),last_ticker_data)
                    continue
                save_price_data(data, ticker,False)
            except Exception as e:
                print(str(e))
                update_ticker_data(ticker, False)
