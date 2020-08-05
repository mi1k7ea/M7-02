# coding=utf-8

from lxml import html
import re

class ResponseChecker:
    def __init__(self, response_text, search_string):
        self.response_text = response_text
        self.search_string = search_string

    def get_check_result(self):
        page_html_tree = html.fromstring(self.response_text)
        results = dict()
        results['payload'] = self.search_string
        results['contexts'] = []

        # 检测属性名，如：<x xxxINPUT=xxx>
        # "//*"是选取文档中的所有元素，"[@xxx]"是选出含有xxx属性名的元素
        xpath = "//*[@" + self.search_string + "]"
        n = page_html_tree.xpath(xpath)
        if len(n):
            context = dict()
            context['type'] = 'attribute_name'
            context['count'] = len(n)
            results['contexts'].append(context)

        # 检测属性值，如：<x xxx=INPUTxxx>
        # "[@*[contains(.,'xxx')]]"是选出属性值包含xxx的所有属性
        xpath = "//*[@*[contains(.,'" + self.search_string + "')]]"
        n = page_html_tree.xpath(xpath)
        if len(n):
            context = dict()
            context['type'] = 'attribute_value'
            context['count'] = len(n)
            results['contexts'].append(context)

        # 检测HTML标签内的内容，如：<x> INPUT </x>
        # "[contains(text(),'xxx')]"是选出内容包含xxx的元素
        xpath = "//*[contains(text(),'" + self.search_string + "')]"
        n = page_html_tree.xpath(xpath)
        if len(n):
            context = dict()
            context['type'] = 'html_tag'
            context['count'] = len(n)
            results['contexts'].append(context)

        # 检测HTML注释中的内容，如：<!--hhhh aaa INPUT -->
        # "[comment()[contains(.,'xxx')]]"是选出包含xxx内容的HTML注释
        xpath = "//*[comment()[contains(.,'" + self.search_string + "')]]"
        n = page_html_tree.xpath(xpath)
        if len(n):
            context = dict()
            context['type'] = 'html_comment'
            context['count'] = len(n)
            results['contexts'].append(context)

        # 检测style标签内容，如：<style>INPUT</style>
        # "//style"是选取style元素
        xpath = "//style[contains(text(),'" + self.search_string + "')]"
        n = page_html_tree.xpath(xpath)
        if len(n):
            context = dict()
            context['type'] = 'style'
            context['count'] = len(n)
            results['contexts'].append(context)

        # 检测style标签属性值，如：<style>.test {INPUT}</style>
        xpath = "//*[@style[contains(.,'" + self.search_string + "')]]"
        n = page_html_tree.xpath(xpath)
        if len(n):
            context = dict()
            context['type'] = 'style_attribute_value'
            context['count'] = len(n)
            results['contexts'].append(context)

        # 检测href属性值，如：<a href=INPUT>a</a>
        xpath = "//*[@href[contains(.,'" + self.search_string + "')]]"
        n = page_html_tree.xpath(xpath)
        if len(n):
            context = dict()
            context['type'] = 'href'
            context['count'] = len(n)
            results['contexts'].append(context)

        # 检测script标签内容，如：<script>INPUT</script>
        xpath = "//script[contains(text(),'" + self.search_string + "')]"
        n = page_html_tree.xpath(xpath)
        if len(n):
            context = dict()
            context['type'] = 'script'
            context['count'] = len(n)
            results['contexts'].append(context)

        # 检测script标签属性值，如：<script xx="INPUT"></script>
        xpath = "//script[@*[contains(.,'" + self.search_string + "')]]"
        n = page_html_tree.xpath(xpath)
        if len(n):
            context = dict()
            context['type'] = 'script_attribute'
            context['count'] = len(n)
            results['contexts'].append(context)

        # 检测script标签中的单双引号内，如：<script>var x='x';</script> <script>var x="x";</script>
        script_single_quote = 0
        script_double_quote = 0
        xpath = "//script[contains(text(),'" + self.search_string + "')]"
        n = page_html_tree.xpath(xpath)
        if len(n):
            for js_finding in n:
                js_string = js_finding.text

                # TODO below line is a mix of Javascript and Python, implement for some rare cases...
                # escaped_search = search.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

                sqre = re.compile("'(?:[^'\\\\]|\\\\.)*" + self.search_string + "(?:[^'\\\\]|\\\\.)*'")
                # sqre = re.compile('\'(?:[^\'\\\\]|\\\\.)*' + escaped_search + '(?:[^\'\\\\]|\\\\.)*\'')
                dqre = re.compile('"(?:[^"\\\\]|\\\\.)*' + self.search_string + '(?:[^"\\\\]|\\\\.)*"')
                # dqre = re.compile('(?:[^"\\\\]|\\\\.)*' + escaped_search + '(?:[^"\\\\]|\\\\.)*"')

                sq = sqre.findall(js_string)
                dq = dqre.findall(js_string)

                script_single_quote += len(sq)
                script_double_quote += len(dq)

            if script_single_quote:
                context = dict()
                context['type'] = 'script_single_quote'
                context['count'] = script_single_quote
                results['contexts'].append(context)

            if script_double_quote:
                context = dict()
                context['type'] = 'script_double_quote'
                context['count'] = script_double_quote
                results['contexts'].append(context)

        # 检测onXXXX()属性事件，如：<a onxxx=INPUT>a</a>
        xpath = '//*[@onerror[contains(.,\'' + self.search_string \
                + '\')] or @onload[contains(.,\'' + self.search_string \
                + '\')] or @onclick[contains(.,\'' + self.search_string \
                + '\')] or @oncontextmenu[contains(.,\'' + self.search_string \
                + '\')] or @ondblclick[contains(.,\'' + self.search_string \
                + '\')] or @onmousedown[contains(.,\'' + self.search_string \
                + '\')] or @onmouseenter[contains(.,\'' + self.search_string \
                + '\')] or @onmouseleave[contains(.,\'' + self.search_string \
                + '\')] or @onmousemove[contains(.,\'' + self.search_string \
                + '\')] or @onmouseover[contains(.,\'' + self.search_string \
                + '\')] or @onmouseout[contains(.,\'' + self.search_string \
                + '\')] or @onmouseup[contains(.,\'' + self.search_string \
                + '\')] or @onkeydown[contains(.,\'' + self.search_string \
                + '\')] or @onkeypress[contains(.,\'' + self.search_string \
                + '\')] or @onkeyup[contains(.,\'' + self.search_string \
                + '\')] or @onabort[contains(.,\'' + self.search_string \
                + '\')] or @onbeforeunload[contains(.,\'' + self.search_string \
                + '\')] or @onhashchange[contains(.,\'' + self.search_string \
                + '\')] or @onpageshow[contains(.,\'' + self.search_string \
                + '\')] or @onpagehide[contains(.,\'' + self.search_string \
                + '\')] or @onresize[contains(.,\'' + self.search_string \
                + '\')] or @onscroll[contains(.,\'' + self.search_string \
                + '\')] or @onunload[contains(.,\'' + self.search_string \
                + '\')] or @onblur[contains(.,\'' + self.search_string \
                + '\')] or @onchange[contains(.,\'' + self.search_string \
                + '\')] or @onfocus[contains(.,\'' + self.search_string \
                + '\')] or @onfocusin[contains(.,\'' + self.search_string \
                + '\')] or @onfocusout[contains(.,\'' + self.search_string \
                + '\')] or @oninput[contains(.,\'' + self.search_string \
                + '\')] or @oninvalid[contains(.,\'' + self.search_string \
                + '\')] or @onreset[contains(.,\'' + self.search_string \
                + '\')] or @onsearch[contains(.,\'' + self.search_string \
                + '\')] or @onselect[contains(.,\'' + self.search_string \
                + '\')] or @ondrag[contains(.,\'' + self.search_string \
                + '\')] or @ondragend[contains(.,\'' + self.search_string \
                + '\')] or @ondragenter[contains(.,\'' + self.search_string \
                + '\')] or @ondragleave[contains(.,\'' + self.search_string \
                + '\')] or @ondragover[contains(.,\'' + self.search_string \
                + '\')] or @ondragstart[contains(.,\'' + self.search_string \
                + '\')] or @ondrop[contains(.,\'' + self.search_string \
                + '\')] or @oncopy[contains(.,\'' + self.search_string \
                + '\')] or @oncut[contains(.,\'' + self.search_string \
                + '\')] or @onpaste[contains(.,\'' + self.search_string \
                + '\')] or @onafterprint[contains(.,\'' + self.search_string \
                + '\')] or @onbeforeprint[contains(.,\'' + self.search_string \
                + '\')] or @onabort[contains(.,\'' + self.search_string \
                + '\')] or @oncanplay[contains(.,\'' + self.search_string \
                + '\')] or @oncanplaythrough[contains(.,\'' + self.search_string \
                + '\')] or @ondurationchange[contains(.,\'' + self.search_string \
                + '\')] or @onemptied[contains(.,\'' + self.search_string \
                + '\')] or @onended[contains(.,\'' + self.search_string \
                + '\')] or @onloadeddata[contains(.,\'' + self.search_string \
                + '\')] or @onloadedmetadata[contains(.,\'' + self.search_string \
                + '\')] or @onloadstart[contains(.,\'' + self.search_string \
                + '\')] or @onpause[contains(.,\'' + self.search_string \
                + '\')] or @onplay[contains(.,\'' + self.search_string \
                + '\')] or @onplaying[contains(.,\'' + self.search_string \
                + '\')] or @onprogress[contains(.,\'' + self.search_string \
                + '\')] or @onratechange[contains(.,\'' + self.search_string \
                + '\')] or @onseeked[contains(.,\'' + self.search_string \
                + '\')] or @onseeking[contains(.,\'' + self.search_string \
                + '\')] or @onstalled[contains(.,\'' + self.search_string \
                + '\')] or @onsuspend[contains(.,\'' + self.search_string \
                + '\')] or @ontimeupdate[contains(.,\'' + self.search_string \
                + '\')] or @onvolumechange[contains(.,\'' + self.search_string \
                + '\')] or @onwaiting[contains(.,\'' + self.search_string \
                + '\')] or @onopen[contains(.,\'' + self.search_string \
                + '\')] or @onmessage[contains(.,\'' + self.search_string \
                + '\')] or @onmousewheel[contains(.,\'' + self.search_string \
                + '\')] or @ononline[contains(.,\'' + self.search_string \
                + '\')] or @onoffline[contains(.,\'' + self.search_string \
                + '\')] or @onpopstate[contains(.,\'' + self.search_string \
                + '\')] or @onshow[contains(.,\'' + self.search_string \
                + '\')] or @onstorage[contains(.,\'' + self.search_string \
                + '\')] or @ontoggle[contains(.,\'' + self.search_string \
                + '\')] or @onwheel[contains(.,\'' + self.search_string \
                + '\')] or @ontouchcancel[contains(.,\'' + self.search_string \
                + '\')] or @ontouchend[contains(.,\'' + self.search_string \
                + '\')] or @ontouchmove[contains(.,\'' + self.search_string \
                + '\')] or @ontouchstart[contains(.,\'' + self.search_string \
                + '\')] or @onsubmit[contains(.,\'' + self.search_string + '\')]]'

        n = page_html_tree.xpath(xpath)
        if len(n):
            context = dict()
            context['type'] = 'on_attribute'
            context['count'] = len(n)
            results['contexts'].append(context)

        return results
