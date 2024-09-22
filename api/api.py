"""api调用类"""
import requests

class API():
    def __init__(self, host, method, headers, uri, body, verify=False):
        self.host = host
        self.method = method
        self.headers = headers
        self.uri = uri
        self.body = body
        self.verify = verify

    def send_request(self):
        url = self.host + self.uri
        if self.method == "GET":
            response = requests.get(url=url, headers=self.headers, params=self.body, verify=self.verify)
        else:
            response = requests.request(url=url, headers=self.headers, method=self.method,
                                        json=self.body, verify=self.verify)

        if self.host == 'https://his.huawei.com': # 某个平台
            if response.json().get('status') == 401:
                raise '某平台登录失效，请替换cookie。' \
            if response.json().get('code') != '00':
                print('url:', url)
                print('body:', self.body)
                print('msg:', response.json())
                raise '某平台接口调用报错，请检查出参msg。'

        return response.json()
