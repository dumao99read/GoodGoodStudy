"""api调用类"""
import requests
requests.packages.urllib3.disable_warnings() # 忽略告警提示

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

        # print(response,type(response))
        # print(response.text)  # 响应回去的文本（字符串）
        # print(response.content)  # 响应回去的内容（二进制），一般用来爬取视频
        # print(response.status_code)  # 响应的状态码
        # print(response.url)  # 获取请求连接地址
        # print(response.cookies)  # 获取返回的cookies信息
        # print(response.cookies.get_dict())  # 获取返回的cookies信息
        # print(response.request)  # 获取请求方式

        # 爬取文档乱码问题
        # print(response.apparent_encoding)  # 文档的编码的方式（从HTML文档找）
        # print(response.encoding)  # 响应体编码方式，eg: response.encoding = response.apparent_encoding  # 文档的声明方式
        #
        # print(response.headers)  # 查看响应头
        # print(response.history)  # 重定向历史   即前一次请求的地址


        if self.host == 'https://m.douban.com': # 某个平台
            if response.status_code != 200:
                raise '豆瓣平台登录失效！'
            # if response.json().get('status') == 401:
            #     raise '某平台登录失效，请替换cookie。'
            # if response.json().get('code') != '00':
            #     print('url:', url)
            #     print('body:', self.body)
            #     print('msg:', response.json())
            #     raise '某平台接口调用报错，请检查出参msg。'



        return response.json()
