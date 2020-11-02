from typing import List, Dict, Tuple
import requests


class Domains(object):
    urls = [
        'http://www.cnnic.cn/download/registar_list/1todayDel.txt',
        'http://www.cnnic.cn/download/registar_list/future1todayDel.txt',
        'http://www.cnnic.cn/download/registar_list/future2todayDel.txt'
    ]
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    }
    proxies = {
        "http": "http://127.0.0.1:2020",
        "https": "http://127.0.0.1:2020",
    }
    register = 'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain={domain}'

    def __init__(self, date: Tuple = (0, 1, 2), file: str = None, proxy: Dict = None) -> None:
        """
        :param date: 需要获取的日期，0，1，2 表示今天，明天，后天删除
        :param file: 读入域名的文件地址
        :param proxy: 获取历史记录的所需的代理
        """
        self._urls = self.urls
        self._headers = self.headers
        self._domains: set = set()
        if file:
            with open(file=file, mode='r') as f:
                self._domains.update([d.strip() for d in f.readlines()])
        for day in date:
            self._download(self._urls[day])

        self._proxies = proxy if proxy else self.proxies
        self._register = self.register

    def _download(self, url) -> None:
        try:
            response = requests.get(url=url, headers=self._headers, verify=False)
            domains = [
                item[1:-1]
                for item
                in response.text.split('\n')[1:]
                if item[1:-4].isalpha() and item.count('.') == 1
            ]
        except requests.exceptions.RequestException:
            self._download(url=url)
        else:
            self._domains.update(domains)

    def set_proxy(self, proxy: Dict):
        self._proxies = proxy

    def filter(self, lengths: List) -> None:
        """
        :param lengths: len(test.cn) -> 7
        """
        _domains = [d for d in self._domains if len(d) in lengths]
        self._domains.clear()
        self._domains.update(_domains)

    def check_register(self):
        for d in self._domains.copy():
            if not self._is_registered(d):
                self._domains.remove(d)

    def _is_registered(self, d):
        try:
            res = requests.get(self._register.format(domain=d))
            return '210' in res.text
        except requests.exceptions.RequestException:
            return self._is_registered(d)
