import json
import time

import requests


def perform_request(method, url, headers=None, data=None):
    try:
        if method == 'GET':
            response = requests.get(url, params=data, headers=headers)
        elif method == 'POST':
            data_json = json.dumps(data)
            response = requests.post(url, data=data_json, headers=headers)
        else:
            raise ValueError("Unsupported HTTP method")
        if response.status_code == 200:
            response_data = response.json()
            # print("Response Data:", response_data)
            return response_data
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
