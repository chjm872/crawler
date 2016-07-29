# coding:utf-8
import sys
import subprocess
import urllib
import urllib2
import cookielib
import random
import re
from flask import Flask, request
# from chaojiying import ChaojiyingClient

app = Flask(__name__)
reload(sys)                         # 2
sys.setdefaultencoding('utf-8')

@app.route('/')
def data_from_captcha():
    host_url = request.args.get('host_url')
    image_url = request.args.get('image_url')
    data_url = request.args.get('data_url')
    post_data = request.args.get('post_data')
    captcha_attr = request.args.get('captcha_attr')
    return fetch_content(host_url, image_url, data_url, post_data, captcha_attr)

def fetch_content(host_url, image_url, data_url, post_data, captcha_attr):
    urlopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()), urllib2.HTTPHandler)
    urllib2.install_opener(urlopener)
    urlopener.addheaders = [('User-Agent',
                             'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.26\
                             61.102 Safari/537.36'), ("Accept", "*/*")]
    # 获取cookie
    response = urlopener.open(host_url)
    result = response.read()
    ls = result.split('PImages?pid=')
    ls = ls[1].split('" alt=""></li>')
    # 获取图片验证码
    iflag = download_file(''.join([image_url, '?pid=', ls[0]]), urlopener)
    if iflag:
        # j_captcha = crack_captcha('captcha.jpg')
        j_captcha = raw_input('输入验证码： ')
        post_data = eval(post_data)
        post_data[captcha_attr] = j_captcha.replace('\n', '')
        post_data['pid'] = ls[0]
        # 查询
        response = urlopener.open(urllib2.Request(data_url, urllib.urlencode(post_data)), timeout=600)
        print response.read().decode('gbk').encode('utf8')
        response = urlopener.open('https://e.szsi.gov.cn/siservice/transUrl.jsp?url=serviceListAction.do?id=1')
        result = response.read()
        ls = result.split('self.location =  "')
        ls = ls[1].split('";')
        response = urlopener.open('https://e.szsi.gov.cn/siservice/'+ls[0])
        return response.read()
    else:
        return 'error'

@app.route('/gd')
def data_from_gd():
    host_url = request.args.get('host_url')
    image_url = request.args.get('image_url')
    data_url = request.args.get('data_url')
    encode_url = request.args.get('encode_url')
    post_data = request.args.get('post_data')
    captcha_attr = request.args.get('captcha_attr')
    return fetch_gd(host_url, image_url, encode_url, data_url, post_data, captcha_attr)

def fetch_gd(host_url, image_url, encode_url, data_url, post_data, captcha_attr):
    urlopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()), urllib2.HTTPHandler)
    urllib2.install_opener(urlopener)
    urlopener.addheaders = [('User-Agent',
                             'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.26\
                             61.102 Safari/537.36'), ("Accept", "*/*")]
    # 获取cookie
    response = urlopener.open(host_url)
    # 获取图片验证码
    iflag = download_file(''.join
                          ([image_url, '?', str(random.randint(1, 99))]), urlopener)
    if iflag:
        j_captcha = crack_captcha_chaojiying('captcha.jpg')
        post_data = eval(post_data)
        post_data[captcha_attr] = j_captcha['pic_str']
        print j_captcha['pic_str']
        print post_data['textfield']
        # 查询
        response = urlopener.open(urllib2.Request(encode_url, urllib.urlencode(post_data)), timeout=600)
        ecode_res = eval(response.read())
        if ecode_res['flag'] == "0":
            chaojiying = ChaojiyingClient()
            chaojiying.report_error(j_captcha['pic_id'])
            return 'error'
        else:
            post_data['textfield'] = ecode_res['textfield']
            response = urlopener.open(urllib2.Request(data_url, urllib.urlencode(post_data)), timeout=600)
            return response.read()
    else:
        return 'error'


def download_file(file_url, urlopener):
    result = False
    try:
        if file_url:
            output_file = open(r'captcha.jpg', 'wb')
            output_file.write(urlopener.open(file_url).read())
            output_file.close()
            result = True
    except IOError, e:
        print e
        result = False
    return result


def crack_captcha(filename):
    subprocess.Popen('tesseract ' + filename + ' result', shell=True, stdout=subprocess.PIPE).wait()
    captcha_result = open('result.txt')
    result_txt = None
    try:
        result_txt = captcha_result.read()
    finally:
        captcha_result.close()
    return result_txt

# def crack_captcha_chaojiying(filename):
#     chaojiying = ChaojiyingClient()
#     image = open(filename, 'rb').read()
#     return chaojiying.post_pic(image, 5000)

if __name__ == '__main__':
    app.run()
