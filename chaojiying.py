#!/usr/bin/env python
# coding:utf-8

import requests
import ConfigParser
from hashlib import md5
import sys


class ChaojiyingClient(object):
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read(sys.path[0]+'/crawler.conf')
        self.username = cf.get('chaojiying', 'username')
        self.password = md5(cf.get('chaojiying', 'password')).hexdigest()
        self.soft_id = '891714'
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def post_pic(self, imagebyte, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', imagebyte)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def report_error(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://code.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()
