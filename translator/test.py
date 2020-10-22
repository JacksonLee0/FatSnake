import random
import requests
import time
import hashlib
import json


class YouDaoTrans(object):

    def __init__(self, keyword):
        self.url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/74.0.3729.131 Safari/537.36 '
        }
        self.keyword = keyword
        self.form_data = {
            "i": keyword,
            "from": "zh_CH",
            "to": "FR",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": self.get_salt(),
            "sign": "",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME",
            "typoResult": "false"
        }

    # js的代码： f = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10)),
    # 通过13位的时间戳加上一个随机的个位数
    # python 中的时间戳是 10位加小数点，可以乘以 1000 取整
    def get_salt(self):
        # 获取时间戳
        timestamp = time.time()
        # 生成salt
        salt = int(timestamp * 1000) + int(random.random() * 10)
        return salt

    # var g = n.md5(u + d + f + c);
    # sign 通多几个数相加然后进行 md5 加密
    def get_sign(self):
        u = self.form_data['client']
        d = self.form_data['i']
        f = self.form_data['salt']
        c = "rY0D^0'nM0}g5Mm1z%1G4"

        str_data = u + str(d) + str(f) + c

        # md5加密
        m = hashlib.md5()
        m.update(str_data.encode('utf-8'))
        sign = m.hexdigest()

        return sign

    # 翻译过程
    def translate(self):
        response = requests.post(self.url, data=self.form_data, headers=self.headers)
        dict_result = json.loads(response.content)
        all_result = ''
        for i in range(len(dict_result['translateResult'][0])):
            all_result += dict_result['translateResult'][0][i]['tgt']
        print(all_result)

    # 开始运行
    def start(self):
        self.form_data['sign'] = self.get_sign()
        self.translate()


if __name__ == '__main__':
    while True:
        keyword = input('请输入要翻译的内容, 输入 need-quit 退出:').replace('\n', '')
        if keyword == 'need-quit':
            break
        youdao = YouDaoTrans(keyword)
        youdao.start()
