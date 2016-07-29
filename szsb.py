# coding:utf-8
# import base64
import crawler

print crawler.fetch_content('https://e.szsi.gov.cn/siservice/LoginAction.do',
                            'https://e.szsi.gov.cn/siservice/PImages',
                            'https://e.szsi.gov.cn/siservice/LoginAction.do',
                            "{'Method': 'P', 'pid': '1467275608859', 'type': '', 'AAC002': 'chjm872',\
                             'CAC222': 'Q29jb2RvZG8xMjM=', 'PSINPUT': ''}", 'PSINPUT').decode('gbk').encode('utf8')
