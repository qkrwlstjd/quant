import time

from scripts.external_services.kis_api import KisApi
from scripts.services.get_buyline import get_buy_condition, get_buy_additional_condition, get_all_ticker_price
from stock.models import Price, Ticker
from stock.services.fetch_finalized_price_data import fetch_finalized_price_data
from stock.services.fetch_last_price_data import fetch_last_date
from stock.services.fetch_ticker_data import fetch_ticker_data
from scripts.services.get_price import get_price
from stock.serializers import PriceSerializer
from datetime import datetime, timedelta

from stock.services.save_price_data import save_price_data
from stock.services.update_ticker_data import update_ticker_data
from util.get_bid_price import get_below_bid_price
from util.safe_int import safe_cast_int


class DailyCron:

    def __init__(self, token=None):
        self.balance = 0
        self.stockBalance = 0
        self.order_list = None
        self.buy_list = None
        self.kis_api = KisApi(env='prod', token=token)
        self.MAX_INVESTMENT = 500000  # 최대 투자 금액을 상수로 선언

    def get_buy_list(self):
        buy_list = []
        tickers = fetch_ticker_data()
        for ticker in tickers:
            today_price = self.kis_api.transe_stock_price(ticker.code)
            if today_price is None:
                continue

            past_price = list((Price.objects.filter(ticker=ticker, is_finalized=True)
                               .order_by('-date'))[:60].values())[::-1]
            combined_prices = past_price + [today_price]
            df = get_buy_condition(combined_prices, 60)
            df = get_buy_additional_condition(df)
            last_row = df.iloc[-1:].copy()
            last_row_json = last_row.to_dict(orient='records')[0]
            if last_row_json["BUY_CONDITION"] and len(str(int(today_price["hts_avls"]))) > 3:
                buy_list.append(last_row_json)

        print(f"매수 확인 수 : {len(buy_list)}")
        return buy_list

    def make_order(self, buy_list):
        remove_order_list = self.kis_api.get_orders()['output']
        order_list = []
        past_order_list = []
        stock_list = self.get_stock_list()
        self.balance = self.kis_api.get_balance()
        self.stockBalance = 0

        for buy in buy_list:
            code = buy["ticker_id"].zfill(6)
            matching_stock = [s for s in stock_list if s["pdno"] == code]
            stock = matching_stock[0] if matching_stock else None
            have_stock_balance = stock["pchs_amt"] if stock else 0
            self.stockBalance = self.stockBalance + int(have_stock_balance)
            hoga_json = {
                'ticker_id': buy['ticker_id'],
                'open': buy['close'],
                'open_1': get_below_bid_price(buy['close']),
                'point': buy['PRICE_CHANGE_POINT'],
                'balance': safe_cast_int(stock["pchs_amt"] if stock else 0)
            }
            if datetime.now().hour == 17 and datetime.now().minute > 30 and hoga_json['balance']*hoga_json['open']<self.MAX_INVESTMENT/(int(datetime.now().minute/10)+1):
                continue
            if self.MAX_INVESTMENT > hoga_json["open"]:
                order_list.append(hoga_json)
        # 1단계: 'point'와 'balance'에 대한 순위 계산
        sorted_by_point = sorted(order_list, key=lambda x: x['point'], reverse=True)
        point_ranks = {item['ticker_id']: rank for rank, item in enumerate(sorted_by_point, start=1)}

        sorted_by_balance = sorted(order_list, key=lambda x: x['balance'], reverse=True)
        balance_ranks = {item['ticker_id']: rank for rank, item in enumerate(sorted_by_balance, start=1)}

        order_list_sorted_by_rank_sum = sorted(order_list, key=lambda x: (
            point_ranks[x['ticker_id']] + balance_ranks[x['ticker_id']], x['point']), reverse=True)

        return order_list_sorted_by_rank_sum

    def post_order(self):


        max_cost = self.MAX_INVESTMENT/10 * self.MAX_INVESTMENT_RATE
        for order in self.order_list:
            if(max_cost-order['balance']<0):
                continue

            order['amount'] = (max_cost-order['balance']) // order['open']
            order['amount'] = order['amount'] if order['amount'] != 0 else 1
            if not ((order['balance'] + order['amount'] * order['open']) > max_cost and order['balance'] != 0):
                self.kis_api.buy_stock(code=order["ticker_id"], price=order["open_1"],
                                       quantity=order["amount"])


    def get_day_price_finalized(self):
        tickers = fetch_ticker_data()
        for ticker in tickers:
            try:
                last_ticker_data = fetch_last_date(ticker, True)
                new_date = last_ticker_data + timedelta(days=1)
                last_ticker_date = new_date.strftime("%Y-%m-%d")  # Convert back to string format
            except Exception as e:
                print(e)
                last_ticker_data = None
                last_ticker_date = None

            default_date = "2020-01-01"
            start_date = last_ticker_date if last_ticker_date else default_date
            if datetime.strptime(start_date, "%Y-%m-%d") > datetime.now():
                continue
            data = fetch_finalized_price_data(ticker.code, ticker.market, start_date)
            try:
                if data == [] and last_ticker_date is None:
                    raise Exception("Not data and last ticker is not")
                if last_ticker_date is not None and str(data[-1]['Date'].strftime('%Y-%m-%d')) == str(last_ticker_data):
                    print(ticker.name, data[-1]['Date'].strftime('%Y-%m-%d'), last_ticker_data)
                    continue
                else:
                    save_price_data(data, ticker, True)
            except Exception as e:
                print(str(e))
                update_ticker_data(ticker, False)

        return True

    def get_day_price_unfinalized(self):
        tickers = fetch_ticker_data()
        for ticker in tickers:
            try:
                last_ticker_data = fetch_last_date(ticker, True)
                new_date = last_ticker_data + timedelta(days=1)
                last_ticker_date = new_date.strftime("%Y-%m-%d")  # Convert back to string format
            except Exception as e:
                print(e)
                last_ticker_data = None
                last_ticker_date = None

            today = datetime.now()
            sixty_days_ago = today - timedelta(days=59)
            formatted_sixty_days_ago = sixty_days_ago.strftime('%Y-%m-%d')
            default_date = formatted_sixty_days_ago

            start_date = last_ticker_date if last_ticker_date else default_date
            if datetime.strptime(start_date, "%Y-%m-%d") > datetime.now():
                continue

            data = fetch_finalized_price_data(ticker.code, ticker.market, start_date)
            try:
                if data == [] and last_ticker_date is None:
                    raise Exception("Not data and last ticker is not")
                if last_ticker_date is not None and str(data[-1]['Date'].strftime('%Y-%m-%d')) == str(last_ticker_data):
                    print(ticker.name, data[-1]['Date'].strftime('%Y-%m-%d'), last_ticker_date)
                    continue
                else:
                    save_price_data(data, ticker, False)
            except Exception as e:
                print(str(e))
                update_ticker_data(ticker, False)
        return True

    def get_stock_list(self):
        stock_list = self.kis_api.get_stock()["output1"]
        stock_list = [stock for stock in stock_list if stock['ord_psbl_qty'] != '0']
        return stock_list

    def sell_stock(self, stock_list):
        for stock in stock_list:
            result = self.kis_api.sell_stock(stock['pdno'], stock['ord_psbl_qty'])
            print(stock["pdno"], stock["prdt_name"], result)
        pass

    def save_ticker_info(self):
        tickers = fetch_ticker_data()
        for ticker in tickers:
            stock_info = self.kis_api.get_stock_price(ticker.code)
            if stock_info is None:
                continue
            ticker.shares = float(stock_info["lstn_stcn"])
            ticker.save()

    def do(self):
        while True:
            current_time = datetime.now()
            # print(current_time)
            self.MAX_INVESTMENT_RATE = (((current_time.hour % 16) * 6  + current_time.minute // 10) + 1)

            if (current_time.hour == 8 and current_time.minute == 40):
                self.kis_api.get_token()
                print(f"{current_time.hour}:{current_time.minute}:::sell_order")
                stock_list = self.get_stock_list()
                self.sell_stock(stock_list)

            if (current_time.hour == 15 and current_time.minute >= 40) or current_time.hour in (16, 17):
                print(f"{current_time.hour}:{current_time.minute}:::get_buy_list")
                if self.buy_list is None:
                    self.buy_list = self.get_buy_list()

            if current_time.hour in (16, 17) and current_time.minute % 10 == 8:
                self.kis_api.cancel_all_orders()
                print(f"{current_time.hour}:{current_time.minute}:::post_order")
                self.order_list = self.make_order(self.buy_list)
                print('orderlist:::', len(self.order_list))
                self.post_order()

            if current_time.hour == 19 and current_time.minute == 0:
                print(f"{current_time.hour}:{current_time.minute}:::get_day_price")
                self.get_day_price_finalized()
                self.get_day_price_unfinalized()
                get_all_ticker_price(recent=True)
                self.buy_list = None

            if current_time.hour//6 == 0 and current_time.minute == 30:
                print(current_time)
                break



            time.sleep(60)
