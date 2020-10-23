#!/usr/bin/python
# -*- coding: UTF-8 -*
# -
import functools
import hashlib
import json
import pymongo
import random
import time
import urllib

import js2py
import requests
import wx
from bs4 import BeautifulSoup

"""
"""
"""
FAT SNAKE 2.7
肥蛇翻译2.7版本更新日志
输入界面范围调整
修复有道bug
"""
"""
"""
version_number = '2.7'

""" YOUDAO TRANSLATOR"""


def getResultYoudao(content):
    url = 'http://www.youdao.com/w/' + urllib.parse.quote(content) + '/#keyfrom=dict2.top'
    req = requests.get(url=url)
    bf = BeautifulSoup(req.text, features="html.parser")
    body = bf.body
    final_text = ''
    try:
        result_contents = body.find('div', class_='results-content')
        if result_contents.find('div', id='phrsListTab', class_='trans-wrapper clearfix') is not None:
            trans_container = body.find('div', class_='trans-container')
            ul = trans_container.find('ul')
            li = ul.find_all('li')
            for item in li:
                try:
                    final_text += item.string + '\n'
                except TypeError as e:
                    pass

            if ul.find_all('p', class_='wordGroup'):
                wordGroup = ul.find_all('p', class_='wordGroup')
                for item in wordGroup:
                    try:
                        span = item.find('span')
                        final_text += span.string + '\n'
                    except TypeError as e:
                        pass
                    contentTitle = item.find_all('span', class_='contentTitle')
                    for word in contentTitle:
                        a = word.find('a', class_='search-js')
                        final_text += a.string + '；'
                final_text += '\n'
            final_text += '(以上来自有道词典)\n'

        if result_contents.find('div', id='webTrans', class_='trans-wrapper trans-tab') is not None:
            sign = False
            wt_container = body.find('div', id='tWebTrans', class_='trans-container tab-content')
            title = wt_container.find_all('div', class_='title')
            for item in title:
                if item.find('span') is not None:
                    span = item.find('span')
                    sign = True
                    final_text += (span.get_text().replace('\n', '').replace(' ', '')) + '\n'

            if sign is True:
                final_text += '(以上来自网络释义)\n'

        if result_contents.find('div', id='ydTrans', class_='trans-wrapper') is not None:
            trans_container = body.find('div', class_='trans-container')
            p = trans_container.find_all('p')
            final_text += p[1].string + '\n'
            final_text += '(以上来自有道翻译)\n'

        if result_contents.find('div', class_='error-wrapper'):
            error = body.find('div', class_='error-typo')
            p = error.find_all('p', class_='typo-rel')
            final_text += '猜您要找的是不是:\n'
            for i in p:
                span = i.find('span', class_='title')
                final_text += span.string + '\n'

        if final_text == '':
            final_text += '(无翻译结果)'
        return final_text
    except AttributeError as e:
        wx.MessageBox('输入内容有误！\n请重新输入！', '提示！', wx.OK | wx.ICON_ERROR)
        return final_text


def getLongTranslationYoudao(content: 'str'):
    timestamp = time.time()
    # 生成salt
    salt = int(timestamp * 1000) + int(random.random() * 10)

    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/74.0.3729.131 Safari/537.36 '
    }
    form_data = {
        "i": content.replace('\n', ''),
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": salt,
        "sign": "",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTlME",
        "typoResult": "false"
    }

    u = form_data['client']
    d = form_data['i']
    f = form_data['salt']
    c = "rY0D^0'nM0}g5Mm1z%1G4"

    str_data = u + str(d) + str(f) + c

    # md5加密
    m = hashlib.md5()
    m.update(str_data.encode('utf-8'))
    sign = m.hexdigest()
    form_data['sign'] = sign

    response = requests.post(url, data=form_data, headers=headers)
    dict_result = json.loads(response.content)
    all_result = ''
    for i in range(len(dict_result['translateResult'][0])):
        all_result += dict_result['translateResult'][0][i]['tgt']
    return all_result + '\n(以上内容来自有道翻译)'


""" GOOGLE TRANSLATOR """


def getResultGoogle(target, sl, tl):
    allText = ['', '', '', '']
    if target == '':
        return ''
    else:
        js = """
                function RL(a, b) {
                    var t = "a";
                    var Yb = "+";
                    for (var c = 0; c < b.length - 2; c += 3) {
                        var d = b.charAt(c + 2),
                        d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
                        d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
                        a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
                    }
                    return a
                }

                function TL(a) {
                    var k = "";
                    var b = 406644;
                    var b1 = 3293161072;

                    var jd = ".";
                    var $b = "+-a^+6";
                    var Zb = "+-3^+b+-f";

                    for (var e = [], f = 0, g = 0; g < a.length; g++) {
                        var m = a.charCodeAt(g);
                        128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
                        e[f++] = m >> 18 | 240,
                        e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
                        e[f++] = m >> 6 & 63 | 128),
                        e[f++] = m & 63 | 128)
                    }
                    a = b;
                    for (f = 0; f < e.length; f++) a += e[f],
                    a = RL(a, $b);
                    a = RL(a, Zb);
                    a ^= b1 || 0;
                    0 > a && (a = (a & 2147483647) + 2147483648);
                    a %= 1E6;
                    return a.toString() + jd + (a ^ b)
                };
        """
        token = js2py.eval_js(js)
        param = {'tk': token(target), 'q': target, 'tl': tl, 'sl': sl}
        result = requests.get("http://translate.google.cn/translate_a/single?client=t&"
                              "hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&source=btn&ssel=0"
                              "&tsel=0&kc=0&ie=UTF-8&oe=UTF-8",
                              params=param)

        text = list(result.json())[0]
        for element in text:
            if element[0] is not None:
                allText[0] += element[0]
        allText[1] += '\n(以上内容来自谷歌翻译)\n'

        if list(result.json())[1] is not None:
            text = list(result.json())[1]
            for element in text:
                allText[2] += element[0] + '.\n'
                allText[2] += '；'.join(element[1]) + '\n'
            allText[3] += '(以上内容来自谷歌词典)'
        return allText


""" INTERFACE """


def versionInfo(event):
    text = """
    ========================================\n
    2.0 版本更新日志:\n
    --- 改名为肥蛇翻译，在这个世界上应该找不到比我的翻译器更帅的名字。\n
    2.1 版本更新日志\n
    --- 新增谷歌翻译英转中。\n
    2.2 版本更新日志:\n
    --- 加入回车键查询单词。\n
    --- 支持有道翻译中英互译。\n
    --- 修复谷歌翻译中转英互译乱码bug。\n
    2.3 版本更新日志:\n
    --- 修复中文输入法下，输入y的单词卡顿问题。\n
    --- 小幅升级用户界面。\n
    2.4 版本更新日志:\n
    --- 增加百度翻译。\n
    --- 有道翻译支持中英互译，百度翻译和谷歌翻译支持多语互译。\n
    2.5 版本更新日志:\n
    --- 移除多语互译中的百度翻译，因为百度翻译太垃圾了，谷歌翻译足以。\n
    --- 界面调整，翻译显示区域增大。\n
    2.6 版本更新日志:\n
    --- 修复在中英互译下，输入过长无法翻译bug。\n
    --- 界面调整，输入区域增大。\n
    2.7 版本更新日志：\n
    --- 在多语互译模式下，加入文本互换功能。\n
    2.7.1 版本更新日志：\n
    --- 修复有道翻译中英互译下的bug。\n
    ========================================\n
    """
    wx.MessageBox(text, 'Fat Snake Translator --version ' + version_number, wx.OK | wx.ICON_NONE)


class Window(wx.Frame):
    def __init__(self, parent, title):
        super(Window, self).__init__(parent, title=title, size=(605, 420))

        self.GoogleLanguageDic = {'中文': 'zh-CN', '英文': 'en', '法语': 'fr', '德语': 'de', '葡萄牙语': 'pt', '西班牙语': 'es',
                                  '意大利语': 'it', '韩语': 'ko', '日语': 'ja', '俄语': 'ru'}

        self.SetMaxSize(size=(605, 420))
        self.SetMinSize(size=(605, 420))
        self.font4label = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName='DengXian')
        self.font4trans = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName='DengXian')
        self.font4btn = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName='DengXian')
        self.font4tfoot = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName='DengXian')

        self.panel = wx.Panel(self)

        '''MAIN ELEMENT'''
        self.mode = wx.ToggleButton(self.panel, label='中英互译', pos=(5, 5), size=(60, 25))
        self.Bind(wx.EVT_TOGGLEBUTTON, self.switchMode, self.mode)

        self.label_1 = wx.StaticText(self.panel, label='请输入查询内容：', pos=(10, 52))
        self.label_1.SetFont(self.font4label)

        self.label_2 = wx.StaticText(self.panel, label='查询结果：', pos=(300, 52))
        self.label_2.SetFont(self.font4label)

        self.input = wx.TextCtrl(self.panel, pos=(10, 105), size=(280, 250), style=wx.TE_MULTILINE | wx.TE_WORDWRAP, )
        self.input.SetFont(self.font4label)
        self.Bind(wx.EVT_TEXT_ENTER, self.doQuery, self.input)

        self.trans = wx.TextCtrl(self.panel, style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_WORDWRAP,
                                 pos=(300, 105), size=(280, 250))
        self.trans.SetFont(self.font4label)

        self.query = wx.Button(self.panel, pos=(170, 50), label='查询 (回车)', size=(112, 25))
        self.query.SetFont(self.font4btn)
        self.Bind(wx.EVT_BUTTON, self.doQuery, self.query)

        self.clean = wx.Button(self.panel, pos=(460, 50), label='清空', size=(112, 25))
        self.clean.SetFont(self.font4btn)
        self.Bind(wx.EVT_BUTTON, self.cleanText, self.clean)
        '''MAIN ELEMENT'''

        '''GOOGLE ELEMENT'''
        sourceList = list(self.GoogleLanguageDic.keys())
        self.sourceLanguage = wx.ComboBox(self.panel, pos=(171, 77), size=(110, 30), value=sourceList[1],
                                          choices=sourceList,
                                          style=wx.TE_READONLY)
        self.sourceLanguage.Hide()

        targetList = list(self.GoogleLanguageDic.keys())
        self.targetLanguage = wx.ComboBox(self.panel, pos=(461, 77), size=(110, 30), value=targetList[0],
                                          choices=targetList,
                                          style=wx.TE_READONLY)
        self.targetLanguage.Hide()

        self.nameLabel_1 = wx.StaticText(self.panel, pos=(9, 33), label='谷歌翻译 ============================'
                                                                        '================================='
                                                                        '===============================')
        self.nameLabel_1.SetFont(self.font4tfoot)
        self.nameLabel_1.Hide()

        self.switch = wx.Button(self.panel, pos=(300, 76), size=(39, 25), label='交换')
        self.Bind(wx.EVT_BUTTON, self.switchText, self.switch)
        self.switch.Hide()

        self.resList = []
        '''GOOGLE ELEMENT'''

        '''YOUDAO ELEMENT'''
        self.nameLabel_2 = wx.StaticText(self.panel, pos=(9, 33), label='有道翻译 ============================'
                                                                        '================================='
                                                                        '===============================')
        self.nameLabel_2.SetFont(self.font4tfoot)

        self.foot = wx.StaticText(self.panel,
                                  label='FAT SNAKE ' + version_number + ' ========================================='
                                                                        '===========================================',
                                  pos=(9, 365))
        self.foot.SetFont(self.font4tfoot)
        '''YOUDAO ELEMENT'''

        self.logButton = wx.Button(self.panel, label='log', pos=(550, 5), size=(35, 25))
        self.Bind(wx.EVT_BUTTON, versionInfo, self.logButton)

        self.Centre()
        self.Show()
        self.Fit()

    def cleanText(self, event):
        self.input.SetLabelText('')
        self.trans.SetLabelText('')

    def doQuery(self, event):
        query = self.input.GetValue()
        if query != '':
            if not self.mode.GetValue():
                if len(query) < 20:
                    resYoudao = getResultYoudao(query)
                else:
                    resYoudao = getLongTranslationYoudao(query)
                self.trans.SetValue(resYoudao)
                # now = time.strftime("%Y-%m-%d %H:%M:%S")
                # collection.insert_one({'_id': now, "originalText": query, "translatedText": resYoudao})
            else:
                sL = self.sourceLanguage.GetValue()
                tL = self.targetLanguage.GetValue()
                if sL == tL:
                    wx.MessageBox('请设置不同的输入语言和输出语言！', '提示！', wx.OK | wx.ICON_INFORMATION)
                else:
                    googleSL = self.GoogleLanguageDic[self.sourceLanguage.GetValue()]
                    googleTL = self.GoogleLanguageDic[self.targetLanguage.GetValue()]
                    self.resList = getResultGoogle(query, googleSL, googleTL)
                    resGoogle = ''.join(map(str, self.resList))
                    self.trans.SetValue(resGoogle)
                    # now = time.strftime("%Y-%m-%d %H:%M:%S")
                    # collection.insert_one({'_id': now, "originalText": query, "translatedText": resGoogle})
        else:
            wx.MessageBox('输入内容为空！\n请重新输入！', '提示！', wx.OK | wx.ICON_INFORMATION)

    def switchMode(self, event):
        self.cleanText(self)
        if not self.mode.GetValue():
            self.mode.SetLabelText('中英互译')
            self.sourceLanguage.Hide()
            self.targetLanguage.Hide()
            self.nameLabel_1.Hide()
            self.nameLabel_2.Show()
            self.switch.Hide()
        else:
            self.nameLabel_2.Hide()
            self.mode.SetLabelText('多语互译')
            self.sourceLanguage.Show()
            self.targetLanguage.Show()
            self.nameLabel_1.Show()
            self.switch.Show()

    def switchText(self, event):
        OriginalLanguage = self.sourceLanguage.GetValue()
        TranslatedLanguage = self.targetLanguage.GetValue()
        if self.trans.GetValue():
            TranslatedText = self.resList[0]
            self.input.SetValue(TranslatedText)
            self.sourceLanguage.SetValue(TranslatedLanguage)
            self.targetLanguage.SetValue(OriginalLanguage)
            self.doQuery(self)


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        begin_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - begin_time
        print('{} 共用时：{} s'.format(func.__name__, run_time))
        return value

    return wrapper


@timer
def my():
    env = pymongo.MongoClient(
        "mongodb+srv://User:12345QWERT@fatsnaketranslator-xooxj.mongodb.net/test?ssl=true&authSource=admin")
    db = env.TranslatorInfo
    collection = db.TranslatedText


if __name__ == '__main__':
    my()
    app = wx.App()
    Window(None, '肥蛇翻译 ' + version_number)
    app.MainLoop()
