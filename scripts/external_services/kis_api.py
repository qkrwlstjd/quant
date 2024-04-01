import os
import requests
import json
import time
from datetime import datetime

from scripts.external_services.base import perform_request
from stock.models import Price


class KisApi:
    def __init__(self, env='dev', token=None):
        self.env_config = self.get_env(env)
        self.token = token
        self.api_rate_limit_num = 10
        self.api_rate_limit_time = 1
        self.request_count = 0
        self.first_request_time = None

    def perform_request(self, method, url, header, data):
        self.check_request_limit()
        try:
            # print('요청',data)
            response = perform_request(method, url, header, data)
            if not response:
                raise Exception('응답이 없습니다.')
            return response
        except Exception as e:
            print(f"Error: {e}, 1초 대기후 재시도",data)
            time.sleep(1)  # 에러 발생 시 10초 대기 후 재시도
            return self.perform_request(method, url, header, data)

    def check_request_limit(self):
        if self.first_request_time is None:
            self.first_request_time = time.time()

        current_time = time.time()
        if self.first_request_time is not None:
            elapsed_time = current_time - self.first_request_time
            if elapsed_time < self.api_rate_limit_time and self.request_count >= self.api_rate_limit_num:
                time.sleep(self.api_rate_limit_time - elapsed_time)
                self.request_count = 0
                self.first_request_time = time.time()

        self.request_count += 1

    def get_env(self, env='dev'):
        if (env == 'prod'):
            return {
                'URL': os.getenv('KIS_URL'),
                'APP_KEY': os.getenv('KIS_APP_KEY'),
                'APP_SECRET': os.getenv('KIS_APP_SECRET')
            }
        else:
            return {
                'URL': os.getenv('KIS_DEV_URL'),
                'APP_KEY': os.getenv('KIS_DEV_APP_KEY'),
                'APP_SECRET': os.getenv('KIS_DEV_APP_SECRET')
            }

    def get_token(self):
        env_config = self.env_config
        # 요청할 URL 설정
        url = f"{env_config['URL']}/oauth2/tokenP"

        # 요청에 사용할 데이터
        data = {
            "grant_type": "client_credentials",
            "appkey": env_config['APP_KEY'],
            "appsecret": env_config['APP_SECRET']
        }

        # Content-Type 지정
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }

        # POST 요청 보내기
        self.token = self.perform_request('POST', url, headers, data)['access_token']
        print(self.token)
        return self.token

    def delete_token(self):
        env_config = self.env_config
        # 요청할 URL 설정
        url = f"{env_config['URL']}/oauth2/revokeP"

        # 요청에 사용할 데이터
        data = {
            "appkey": env_config['APP_KEY'],
            "appsecret": env_config['APP_SECRET'],
            'token': self.token
        }

        # Content-Type 지정
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }

        data_json = json.dumps(data)

        # POST 요청 보내기
        self.token = self.perform_request('POST', url, headers, data_json)
        return self.token

    def get_stock_price(self, code):
        code = code.zfill(6)
        # 환경 설정 가져오기
        env_config = self.env_config

        # 요청할 URL 설정
        url = f"{env_config['URL']}/uapi/domestic-stock/v1/quotations/inquire-price"

        # 요청에 사용할 데이터
        data = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": code,
        }
        token = self.token if self.token else self.get_token()

        # Content-Type 지정
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'authorization': f"Bearer {token}",
            'appkey': env_config['APP_KEY'],
            'appsecret': env_config['APP_SECRET'],
            'tr_id': 'FHKST01010100'
        }

        return self.perform_request('GET', url, headers, data)['output']

    def transe_stock_price(self, code):
        stock_info = self.get_stock_price(code)
        if stock_info["iscd_stat_cls_code"] == '58':
            return None
        price = {
            'ticker_id': code,
            'high': float(stock_info['stck_hgpr']),
            'low': float(stock_info['stck_lwpr']),
            'open': float(stock_info['stck_oprc']),
            'close': float(stock_info['stck_prpr']),
            'volume': float(stock_info['acml_vol']),
            'hts_avls': str(int(stock_info['hts_avls'])),
            'is_finalized': True,
            'date': datetime.now().date(),
        }
        return price

    def get_stock_time_over(self, code):
        code = code.zfill(6)
        # 환경 설정 가져오기
        env_config = self.env_config

        # 요청할 URL 설정
        url = f"{env_config['URL']}/uapi/domestic-stock/v1/quotations/inquire-time-overtimeconclusion"

        # 요청에 사용할 데이터
        data = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": code,
            "FID_HOUR_CLS_CODE": 1,
        }
        token = self.token if self.token else self.get_token()

        # Content-Type 지정
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'authorization': f"Bearer {token}",
            'appkey': env_config['APP_KEY'],
            'appsecret': env_config['APP_SECRET'],
            'tr_id': 'FHPST02310000'
        }

        return self.perform_request('GET', url, headers, data)

    def get_max_buy_amount(self, code, price):
        code = code.zfill(6)
        # 환경 설정 가져오기
        env_config = self.env_config

        # 요청할 URL 설정
        url = f"{env_config['URL']}/uapi/domestic-stock/v1/trading/inquire-psbl-order"

        # 요청에 사용할 데이터
        data = {
            "CANO": "46821316",
            "ACNT_PRDT_CD": "01",
            "PDNO": code,
            "ORD_UNPR": price,
            "ORD_DVSN": "07",
            "CMA_EVLU_AMT_ICLD_YN": "Y",
            "OVRS_ICLD_YN": "Y",
        }
        token = self.token if self.token else self.get_token()

        # Content-Type 지정
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'authorization': f"Bearer {token}",
            'appkey': env_config['APP_KEY'],
            'appsecret': env_config['APP_SECRET'],
            'tr_id': 'TTTC8908R',
        }

        return self.perform_request('GET', url, headers, data)

    def buy_stock(self, code, price, quantity):
        code = code.zfill(6)
        # 환경 설정 가져오기
        env_config = self.env_config

        # 요청할 URL 설정
        url = f"{env_config['URL']}/uapi/domestic-stock/v1/trading/order-cash"

        # 요청에 사용할 데이터
        data = {
            "CANO": "46821316",
            "ACNT_PRDT_CD": "01",
            "PDNO": code,
            "ORD_DVSN": "07",
            "ORD_QTY": str(int(quantity)),
            "ORD_UNPR": str(int(price)),

        }
        token = self.token if self.token else self.get_token()

        # Content-Type 지정
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'authorization': f"Bearer {token}",
            'appkey': env_config['APP_KEY'],
            'appsecret': env_config['APP_SECRET'],
            'tr_id': 'TTTC0802U',
            "custtype": "P"
        }

        return self.perform_request('POST', url, headers, data)

    def get_orders(self):
        # 환경 설정 가져오기
        env_config = self.env_config

        # 요청할 URL 설정
        url = f"{env_config['URL']}/uapi/domestic-stock/v1/trading/inquire-psbl-rvsecncl"

        # 요청에 사용할 데이터
        data = {
            "CANO": "46821316",
            "ACNT_PRDT_CD": "01",
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
            "INQR_DVSN_1": "0",
            "INQR_DVSN_2": "0",
        }
        token = self.token if self.token else self.get_token()

        # Content-Type 지정
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'authorization': f"Bearer {token}",
            'appkey': env_config['APP_KEY'],
            'appsecret': env_config['APP_SECRET'],
            'tr_id': 'TTTC8036R',
        }

        return self.perform_request('GET', url, headers, data)

    def cancle_order(self, order):
        # 환경 설정 가져오기
        env_config = self.env_config

        # 요청할 URL 설정
        url = f"{env_config['URL']}/uapi/domestic-stock/v1/trading/order-rvsecncl"

        # 요청에 사용할 데이터
        data = {
            "CANO": "46821316",
            "ACNT_PRDT_CD": "01",
            "RVSE_CNCL_DVSN_CD": "02",
            "QTY_ALL_ORD_YN": "Y",
            "ORD_QTY": "0",
            "ORD_UNPR": "0",
            "KRX_FWDG_ORD_ORGNO": "",
            "ORGN_ODNO": str(order["odno"]),  # 원주문번호
            "ORD_DVSN": str(order["ord_dvsn_cd"]),  # 주문구분
        }

        token = self.token if self.token else self.get_token()

        # Content-Type 지정
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'authorization': f"Bearer {token}",
            'appkey': env_config['APP_KEY'],
            'appsecret': env_config['APP_SECRET'],
            'tr_id': 'TTTC0803U',
            "custtype": "P"
        }

        return self.perform_request('POST', url, headers, data)

    def cancel_all_orders(self):
        orders = self.get_orders()["output"]
        for order in orders:
            result = self.cancle_order(order)
            print(result)
        return

    def get_stock(self):
        # 환경 설정 가져오기
        env_config = self.env_config

        # 요청할 URL 설정
        url = f"{env_config['URL']}/uapi/domestic-stock/v1/trading/inquire-balance"

        # 요청에 사용할 데이터
        data = {
            "CANO": "46821316",
            "ACNT_PRDT_CD": "01",
            "AFHR_FLPR_YN": "N",
            "OFL_YN": "",
            "INQR_DVSN": "Y",
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": "N",
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": "00",
            "CTX_AREA_NK100": "",
            "CTX_AREA_FK100": "",
        }
        token = self.token if self.token else self.get_token()

        # Content-Type 지정
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'authorization': f"Bearer {token}",
            'appkey': env_config['APP_KEY'],
            'appsecret': env_config['APP_SECRET'],
            'tr_id': 'TTTC8434R',
        }

        return self.perform_request('GET', url, headers, data)

    def sell_stock(self, code, quantity):
        code = code.zfill(6)
        # 환경 설정 가져오기
        env_config = self.env_config

        # 요청할 URL 설정
        url = f"{env_config['URL']}/uapi/domestic-stock/v1/trading/order-cash"

        # 요청에 사용할 데이터
        data = {
            "CANO": "46821316",
            "ACNT_PRDT_CD": "01",
            "PDNO": code,
            "ORD_DVSN": "01",
            "ORD_QTY": str(int(quantity)),
            "ORD_UNPR": "0",

        }
        token = self.token if self.token else self.get_token()

        # Content-Type 지정
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'authorization': f"Bearer {token}",
            'appkey': env_config['APP_KEY'],
            'appsecret': env_config['APP_SECRET'],
            'tr_id': 'TTTC0801U',
            "custtype": "P"
        }

        return self.perform_request('POST', url, headers, data)


    def get_balance(self):
        # 환경 설정 가져오기
        env_config = self.env_config

        # 요청할 URL 설정
        url = f"{env_config['URL']}/uapi/domestic-stock/v1/trading/inquire-account-balance"

        # 요청에 사용할 데이터
        data = {
            "CANO": "46821316",
            "ACNT_PRDT_CD": "01",
            "INQR_DVSN_1": "",
            "BSPR_BF_DT_APLY_YN": "",
        }
        token = self.token if self.token else self.get_token()

        # Content-Type 지정
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'authorization': f"Bearer {token}",
            'appkey': env_config['APP_KEY'],
            'appsecret': env_config['APP_SECRET'],
            'tr_id': 'CTRP6548R',
        }

        return int(self.perform_request('GET', url, headers, data)['output2']['tot_asst_amt'])
