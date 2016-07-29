# coding:utf-8
# import base64
import requests

headers = {
    'Connection': 'Keep-Alive',
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
}


def login():
    j_captcha = raw_input('输入验证码：')
    j_captcha = j_captcha.replace('\n', '')
    params = {
        "app_version": 1,
        "app_channel": "WAP",
        "device_info": 123,
        "fund_code": "perAccoLogin",
        "timestamp": 1467769536661,
        "sign": "10173196ec4159550c941337d9fbe7f6",
        "data_entity": "{\"AccNum\":\"20600889588\",\"QryPwd\":\"a9hemuOKMzv92IvFX21bYyKvtjuiDGYDIyvZPY4ob4OIgqSipSmmRO/Xl0Q7oGFsV03LqONPDf2ttBfTEcfi4sbbssI/cnphI8t99eULeFL72kFMnmQBlkk8W+ZeQuMLTP2WwHGUosR10jDl8H7CZOsNJo80k2mZRKaQeR0p+kI=\",\"Token\":" + j_captcha + ",\"TranFlag\":\"1\",\"timestamp\":1467769536661,\"verify_type\":\"1\"}"
    }
    r = requests.post('https://weixin.szzfgjj.com/WheatInterface/in', data=params, headers=headers)
    return r.json()


def download_file(file_url):
    result = False
    try:
        if file_url:
            output_file = open(r'captcha.jpg', 'wb')
            output_file.write(requests.get(file_url, stream=True, headers=headers).content)
            output_file.close()
            result = True
    except IOError, e:
        print e
        result = False
    return result


if __name__ == '__main__':
    download_file("https://weixin.szzfgjj.com/WheatInterface/in?app_version=1&app_channel=WAP&device_info=123&fund_code=base_show_picvcode&timestamp=1467771829202&sign=0d61b18d38467e47512f8d6eff8b5bcd&data_entity={%22timestamp%22:1467771829202,%22verify_type%22:%221%22}")
    print login()['ret_msg']
