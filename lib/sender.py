# coding-utf-8

import requests

def send(request, scheme):
    url = "{}://{}{}".format(scheme, request.headers.get("host"), request.path)
    if request.headers.get('cookie'):
        cookies = dict()
        cookie_list = request.headers.get('cookie').split(';')
        print(cookie_list)
        for cookie_index in cookie_list:
            key = cookie_index.split('=')[0]
            index = cookie_index.index('=') + 1
            value = cookie_index[index:]
            cookies[key] = value
        req = requests.Request(request.method, url, params=request.params, data=request.post_data, cookies=cookies)
    else:
        req = requests.Request(request.method, url, params=request.params, data=request.post_data)
    r = req.prepare()
    s = requests.Session()
    response = s.send(r, allow_redirects=False, verify=False)
    return response

def makeRequest(request):
    try:
        rawRequest = ''
        request_query = ''
        for q in request.query:
            if request_query != '':
                request_query += "&"
            line = q + "=" + request.query[q]
            request_query += line
        rawRequest += str(request.method) + ' ' + str(request.path) + "?" + request_query + ' ' + str(
            request.http_version)
        for k, v in request.headers.items():
            rawRequest += '\r\n'
            rawRequest += str(k) + ': ' + str(v)

        rawRequest += '\r\n\r\n'
        if request.get_text():
            rawRequest += request.get_text()

        return rawRequest

    except Exception as e:
        raise Exception(e)