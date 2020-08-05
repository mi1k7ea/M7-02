# coding=utf-8

import copy

from lib.conf import TEST_CASE

class GetInsertPoints:
    def __init__(self, request):
        self.request = request
        self.requests = []
        self.insert_params(append=True)
        self.insert_post_data(append=True)

    def insert_params(self, append: bool = False) -> None:
        if self.request.params:
            for data in self.request.params:
                request = copy.deepcopy(self.request)
                if append:
                    request.params[data] = str(request.params[data]) + TEST_CASE
                else:
                    request.params[data] = TEST_CASE
                request.insert_param = data
                request.insert_place = 'query'
                self.requests.append(request)

    def insert_post_data(self, append: bool = False) -> None:
        if self.request.post_data:
            for data in self.request.post_data:
                request = copy.deepcopy(self.request)
                if append:
                    request.post_data[data] = str(request.post_data[data]) + TEST_CASE
                else:
                    request.post_data[data] = TEST_CASE
                request.insert_param = data
                request.insert_place = "body"
                self.requests.append(request)
