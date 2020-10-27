from typing import List, Dict

import requests


class Domains(object):
    def __init__(self, use_proxy=False):
        self._today_url = 'http://www.cnnic.cn/download/registar_list/1todayDel.txt'
        self._tomorrow_url = 'http://www.cnnic.cn/download/registar_list/future1todayDel.txt'
        self._next_tomorrow_url = 'http://www.cnnic.cn/download/registar_list/future2todayDel.txt'
        self._headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        }
        self.use_proxy = use_proxy
        self._proxies = {
            "http": "http://127.0.0.1:2020",
            "https": "http://127.0.0.1:2020",
        }
        self._today_domains: List = self.download(self._today_url)
        self._tomorrow_domains: List = self.download(self._tomorrow_url)
        self._next_tomorrow_domains: List = self.download(self._next_tomorrow_url)

    def get_today_domains(self, max_length=10):
        return self._get_domains(domains=self._today_domains, max_length=max_length)

    def get_tomorrow_domains(self, max_length=10):
        return self._get_domains(domains=self._tomorrow_domains, max_length=max_length)

    def get_next_tomorrow_domains(self, max_length=10):
        return self._get_domains(domains=self._next_tomorrow_domains, max_length=max_length)

    @staticmethod
    def _get_domains(domains: List, max_length: int):
        tmp_domains: List = [domain for domain in domains if len(domain) < max_length + 4]
        tmp_domains.sort()
        return tmp_domains

    def download(self, url) -> list:
        try:
            if self.use_proxy:
                response = requests.get(url=url, headers=self._headers, proxies=self._proxies, verify=False)
            else:
                response = requests.get(url=url, headers=self._headers, verify=False)
            domains = [
                item[1:-1]
                for item
                in response.text.split('\n')[1:]
                if item[1:-4].isalpha() and item.count('.') == 1
            ]
        except requests.exceptions.RequestException:
            return self.download(url=url)
        else:
            return domains

    def set_proxies(self, proxy: Dict):
        """
        :param proxy: 支持 str 和 dict
        :return: None
        """
        if isinstance(proxy, str):
            protocol, _ = proxy.split(':', maxsplit=1)
            proxy: Dict = {
                protocol: proxy
            }
        self._proxies = proxy
