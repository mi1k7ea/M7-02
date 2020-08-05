# coding=utf-8

import urllib3
urllib3.disable_warnings()

import copy
from lxml import html
import mitmproxy.http

from lib.http_request_parser import RequestParser
from lib.sender import send, makeRequest
from lib.conf import TEST_CASE
from xssscaner.inject_test_case import GetInsertPoints
from xssscaner.response_checker import ResponseChecker
from xssscaner.payload_generator import payload_generate

class Proxy:
    def request(self, flow: mitmproxy.http.HTTPFlow):
        raw_request = bytes(makeRequest(flow.request), encoding="utf8")

        parser = RequestParser(raw_request)
        points = GetInsertPoints(parser)

        for request in points.requests:
            response = send(request, flow.request.scheme)

            # 检测注入测试用例后的响应报文中是否存在测试用例字样
            if TEST_CASE in response.text:
                print("\n[*]Test case is found in", request.insert_place)
                checker = ResponseChecker(response.text, TEST_CASE)
                result = checker.get_check_result()

                # 如果响应中存在测试用例字样，则根据字样出现的位置替换成相应的payload来进行XSS攻击
                payload_list = []
                for context in result["contexts"]:
                    print(context)
                    payloads = payload_generate(context['type'])

                    for payload in payloads:
                        xss_request = copy.deepcopy(request)
                        xss_request.replace(TEST_CASE, payload['payload'])
                        response = send(xss_request, "http")

                        # 不对3xx、4xx、5xx进行处理
                        if response.status_code == 200:
                            page_html_tree = html.fromstring(response.text)
                            count = page_html_tree.xpath(payload['find'])
                            if len(count):
                                payload_list.append(payload['payload'])
                        else:
                            print("[-]Response status code wrong.")

                # 如果检测到XSS payload在响应报文中，则判定存在漏洞
                if len(payload_list) > 0:
                    with open("./result/result.txt", "a+") as f:
                        print("[+]Found a Reflection XSS:", flow.request.url)
                        if request.insert_place == 'query':
                            print("[+]Inject Point in URL Query Parameter:", request.insert_param)
                        else:
                            print("[+]Inject Point in Body Parameter:", request.insert_param)

                        # 保存结果到./result/result.txt中
                        f.write(request.method + " " + flow.request.url + "\n")
                        f.write("Vulnerable Param: " + request.insert_param + "\n")
                        f.write("Payload:\n")

                        print("[+]Payload:")
                        for payload in payload_list:
                            print("  ", payload)
                            f.write("  " + payload + "\n")
                        f.write("\n")
                        print()

addons = [
	Proxy(),
]
