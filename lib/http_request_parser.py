# coding=utf-8

from http.server import BaseHTTPRequestHandler
from io import BytesIO
from urllib import parse


# 使用Python自带的http库来解析请求
# HTTPRequest类，继承自BaseHTTPRequestHandler类
class HTTPRequest(BaseHTTPRequestHandler):
    # 构造函数从文本中读取HTTP Request内容并进行解析
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = None
        self.error_message = None
        self.parse_request()

    def send_error(self, code, message=None, explain=None):
        self.error_code = code
        self.error_message = message


# RequestParser类
class RequestParser(object):
    def __init__(self, request_text):
        try:
            self.raw_request = HTTPRequest(request_text)
            if self.raw_request.error_code:
                raise Exception(self.raw_request.error_message)
            self.method = self.raw_request.command
            self.path = self.get_path()
            self.headers = self.raw_request.headers
            self.post_data = self.convert(self.get_postdata())
            self.params = self.convert(self.get_params())
        except Exception as e:
            raise e

    # 数据类型转换
    def convert(self, data):
        if isinstance(data, bytes):
            return data.decode()
        if isinstance(data, (str, int)):
            return str(data)
        if isinstance(data, dict):
            # 通过map()来对data内的元素调用convert()处理
            return dict(map(self.convert, data.items()))
        if isinstance(data, tuple):
            return tuple(map(self.convert, data))
        if isinstance(data, list):
            return list(map(self.convert, data))
        if isinstance(data, set):
            return set(map(self.convert, data))

    # 获取URL路径
    def get_path(self):
        return parse.urlsplit(self.raw_request.path).path

    # 将Body和URL请求参数保存为dict，方便后续解析和添加payload
    # 获取POST请求内容
    def get_postdata(self):
        # GET请求不存在Body，也就无CL头
        if 'Content-Length' in self.raw_request.headers.keys():
            content_length = int(self.raw_request.headers.get('Content-Length'))
            return dict(parse.parse_qsl(self.raw_request.rfile.read(content_length)))
        else:
            return dict()

    # 获取URL参数
    def get_params(self):
        url_param = parse.urlsplit(self.raw_request.path).query
        return dict(parse.parse_qsl(url_param))

    # 在http头字段、URL参数和POST内容中替换XSS payload
    def replace(self, string, payload):
        for key, value in self.headers.items():
            key.replace(string, payload)
            value.replace(string, payload)

        for key, value in self.params.items():
            self.params[key] = self.params[key].replace(string, payload)

        for key, value in self.post_data.items():
            self.post_data[key] = self.post_data[key].replace(string, payload)
