# coding=utf-8
import re
import requests
from lxml import etree
from ProxyPool.utils import parse_url

"""
目前内置爬取的第三方IP代理商如下：

"""
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}


class ProxyMetaclass(type):
    """
    元类，在ProxyGetter类中加入
    __SpiderFunc__和__SpiderFuncCount__两个参数
    分别表示爬虫函数和爬虫函数的数量
    """

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__SpiderFunc__'] = []
        for k in attrs.keys():
            if k.startswith('spider_'):  # def spider_data5u():
                attrs['__SpiderFunc__'].append(k)
                count += 1
        attrs['__SpiderFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class ProxyGetter(object, metaclass=ProxyMetaclass):
    """
    目前内置爬取的第三方IP代理商如下：

    """

    def get_raw_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('Getting', proxy, 'from', callback)
            proxies.append(proxy)
        return proxies

    def spider_66ip(self):
        """
        66免费代理网(不确定是不是高匿的，不过正常使用没有影响)
        http://www.66ip.cn/
        """
        url_list = [
            "http://www.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=",
            "http://www.66ip.cn/nmtq.php?getnum={}&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0"
            "&proxytype=2&api=66ip"
        ]
        for url in url_list:
            html = parse_url(url)
            try:
                ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", html)
                for ip in ips:
                    yield ip.strip()
                    # print(ip.strip())
            except Exception as e:
                print(e)

    def spider_xicidaili(self):
        """
        西刺代理
        http://www.xicidaili.com
        """
        url_list = [
            "https://www.xicidaili.com/nn/"
        ]
        for url in url_list:
            try:
                html = parse_url(url)
                html_tree = etree.HTML(html)
                proxy_list = html_tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        yield ":".join(proxy.xpath('./td/text()')[0:2])
                        # print(":".join(proxy.xpath('./td/text()')[0:2]))
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)

    def spider_data5u(self):
        """
        无忧代理
        http://www.data5u.com/
        """
        url_list = ["http://www.data5u.com/"]
        for url in url_list:
            try:
                html = requests.get(url=url, headers=headers).content
                html_tree = etree.HTML(html)
                ul_list = html_tree.xpath('//ul[@class="l2"]')
                for ul in ul_list:
                    try:
                        ip = ul.xpath('./span[1]/li/text()')[0]
                        port = ul.xpath('./span[2]/li/text()')[0]
                        high_anonymity = True if ul.xpath('./span[3]/li/text()')[0] == "高匿" else False
                        if high_anonymity:
                            yield '{}:{}'.format(ip, port)
                            # print('{}:{}'.format(ip, port))
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)

    def spider_kuaidaili(self):
        """
        快代理
        https://www.kuaidaili.com/
        """
        for page in range(1, 4):
            url = 'http://www.kuaidaili.com/free/inha/{}/'.format(page)
            resp = parse_url(url)
            try:
                html = etree.HTML(resp)
                ips = html.xpath('//*[@id="list"]/table/tbody/tr/td[1]/text()')
                ports = html.xpath('//*[@id="list"]/table/tbody/tr/td[2]/text()')
                for ip, port in zip(ips, ports):
                    proxy = ip + ':' + port
                    yield proxy
            except Exception as e:
                print(e)


if __name__ == '__main__':
    pass
