import os
import requests
import json
import time

from scripts.external_services.base import perform_request


class KisApi:
    def __init__(self, env='dev'):
        self.env_config = self.get_env(env)
        self.token = None
        self.api_rate_limit_num = 10
        self.api_rate_limit_time = 2
        self.request_count = 0
        self.first_request_time = None

    def perform_request(self, method, url, header, data):
        self.check_request_limit()
        try:
            response = perform_request(method, url, header, data)
            if not response:
                raise Exception('응답이 없습니다.')
            return response
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)  # 에러 발생 시 10초 대기 후 재시도
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

        data_json = json.dumps(data)

        # POST 요청 보내기
        self.token = self.perform_request('POST', url, headers, data_json)['access_token']
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
