# M7-02
个人使用的基于mitmproxy的被动RXSS扫描器，是学习mitmproxy的时候开发的。没错，就是个鸡肋漏洞被动扫描器，只是为了验证个人想法的可行性才搞的，但是可以方便地在浏览站点的时候自动挖掘一些RXSS，还是有点用的。

关于mitmproxy这个中间人攻击代理工具直接看官方文档的就可以了。

mitmproxy安装：pip3 install mitmproxy

扫描原理：自定义mitmproxy插件，将代理的请求下发给BaseHTTPRequestHandler继承类进行请求报文解析，然后替换URL query、Body、Header中的参数值为测试用例值，在响应中通过XPath解析检测到该用例值后就替换为XSS payload重放报文，如果响应报文中通过XPath解析得到XSS payload则报存在反射型XSS漏洞。

使用方法：

```powershell
python m7-02.py
```

注意：**这里的RXSS检测规则是参考GitHub上的某个开源项目，具体细化的规则可自行添加，并且还不支持JSONP反射型XSS的检测。**

扫描效果：

```powershell
PS M:\M7-02> python m7-02.py                                                                             

        _|      _|  _|_|_|_|_|                _|      _|_|
        _|_|  _|_|          _|              _|  _|  _|    _|
        _|  _|  _|        _|    _|_|_|_|_|  _|  _|      _|
        _|      _|      _|                  _|  _|    _|
        _|      _|    _|                      _|    _|_|_|_|  v1.0


[*]Please select a way to start mitm on Windows:
  1.mitmdump
  2.mitmweb
[*]Choose: 2
[*]Startup mitmweb and load addon...
Web server listening at http://127.0.0.1:8081/
Loading script M:/M7-02/mitm_addon.py
Proxy server listening at http://*:8080
127.0.0.1:54206: clientconnect
127.0.0.1:54209: clientconnect
127.0.0.1:54211: clientconnect
127.0.0.1:54213: clientconnect
127.0.0.1:54214: clientconnect
127.0.0.1:54206: clientdisconnect

[*]Test case is found in body
{'type': 'html_tag', 'count': 1}
[+]Found a Reflection XSS: http://testphp.vulnweb.com/search.php?test=query
[+]Inject Point in Body Parameter: searchFor
[+]Payload:
   <svg onload=prompt`812132`>

127.0.0.1:54209: clientdisconnect
127.0.0.1:54211: clientdisconnect
[*]User aborted.
[*]Passive Reflection XSS scan result is saved in: ./result/result.txt
PS M:\M7-02> type result/result.txt
POST http://testphp.vulnweb.com/search.php?test=query
Vulnerable Param: searchFor
Payload:
  <svg onload=prompt`812132`>

PS M:\M7-02>                                                       
```

