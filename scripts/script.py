from scripts.services.get_atr_result import get_atr_result, calc
from scripts.services.get_buy_info import get_correlation
from scripts.services.get_buyline import get_all_ticker_price
from stock.services.fetch_ticker_data import fetch_ticker_data
import pandas as pd
from scripts.services.get_talib import get_talib
from scripts.services.get_today_buyline import DailyCron


# get_buy_info()
# fetch_ticker_info()
def main_script():

    # cron = DailyCron(token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjE1NDFiMWFjLTA2Y2UtNDk5Ny05ZTI1LWE0OTAzOTUwY2M2YSIsImlzcyI6InVub2d3IiwiZXhwIjoxNzA4NTIwMTA4LCJpYXQiOjE3MDg0MzM3MDgsImp0aSI6IlBTbXQ4ck4xQld5c3JsSUVZSWRJZ0M0a2RBZWJaWHRjdHBkaiJ9.FoG5wz3yVheNIV63-BnQ7YXeGRuYX_ci7ycrdRnyP3XxRkRDSx3zH2-hkVcT2EFfkBNd1Ybb3Mx7dOTLoVjifg')
    # cron.get_day_price_finalized()
    # cron.get_day_price_unfinalized()
    cron = DailyCron()
    # a= cron.get_buy_list()
    # print(a)
    cron.do()
    # a=cron.kis_api.get_balance()
    # print(a)
    # cron.s  ave_ticker_info()
    # sl=cron.get_stock_list()
    # cron.sell_stock(sl)
    # get_all_ticker_price(recent=True,test=True)
    #
    # calc()

    # get_talib()
    # get_correlation()

    # _type = 'mix'
    # test_cron_job_execution()
    # get_all_ticker_price(limit=60, _type=_type)



    # results = get_atr_result(comment='mix_60').values()
    # df = pd.DataFrame(results)
    # correlation = df['profit'].corr(df['volume'])
    # print(f"Profit과 volume 간의 상관계수: {correlation}")
    # correlation = df['profit'].corr(df['calculation'])
    # print(f"Profit과 calculation 간의 상관계수: {correlation}")

    # get_talib()
    # get_correlation()
