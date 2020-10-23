#!/usr/bin/python
# -*- coding: UTF-8 -*
# -
import json
import re
import urllib

import js2py
import requests
import wx
from bs4 import BeautifulSoup

"""
"""
"""
FAT SNAKE 2.4
肥蛇翻译2.4版本更新日志
1. 加入百度翻译
"""
"""
"""

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
                        print(span.string)
                        final_text += span.string + '\n'
                    except TypeError as e:
                        pass
                    contentTitle = item.find_all('span', class_='contentTitle')
                    for word in contentTitle:
                        a = word.find('a', class_='search-js')
                        final_text += a.string + '；'
                        print(a.string)
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
                    final_text += (span.string.strip()) + '\n'

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


""" GOOGLE TRANSLATOR """


def getResultGoogle(target, sl, tl):
    allText = ''
    if target == '':
        return allText
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
        print(token.constructor)
        # model = re.compile(u'[\u4e00-\u9fa5]')
        #
        # if model.search(target):
        #     tl = 'en'
        # else:
        #     tl = 'zh-CN'

        param = {'tk': token(target), 'q': target, 'tl': tl, 'sl': sl}
        result = requests.get("http://translate.google.cn/translate_a/single?client=t&"
                              "hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&source=btn&ssel=0"
                              "&tsel=0&kc=0&ie=UTF-8&oe=UTF-8",
                              params=param)

        if list(result.json())[1] is None:
            text = list(result.json())[0]
            for element in text:
                if element[0] is not None:
                    allText += element[0] + '\n'
        else:
            text = list(result.json())[1]
            for element in text:
                allText += element[0] + '.\n'
                allText += '；'.join(element[1]) + '\n'
        allText += '(以上内容来自谷歌翻译)'
        return allText


"""BAIDU TRANSLATOR"""


def getResultBaidu(content, sl, tl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.98 Safari/537.36',
        'Cookie': 'BIDUPSID=E9B058D087F0C0FDD3A0C88A93681FCE; PSTM=1536569393; '
                  'BDUSS=zFYV1NpRVRmSDhEVWg2Y3pjS2t5RFdXWGFoa0NIeFROdnozdWRkWU1MZHB2T3RiQVFBQUFBJCQAAAAAAAAAAAEAAADnj6yvtdK~y83GtuA5NQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGkvxFtpL8RbM; MCITY=-%3A; BAIDUID=0A5182736E61ACA3D7442FC0DDE62F01:FG=1; BDSFRCVID=bV4sJeCCxG3J_p59aEDMQwqW21UdQvfiKQYI3J; H_BDCLCKID_SF=JRA8oK05JIvhDRTvhCcjh-FSMgTBKI62aKDsKp7g-hcqEIL4LPRbQR0pjnOJBnOfQmTH2DQma4OkHUbSj4Qoj-6QbfvLBTolLeJMXJRttq5nhMJm257JDMP0qJ7jttTy523ibR6vQpnNqxtuj6tWj6j0DNR22Pc22-oKWnTXbRu_Hn7zeUjoDbtpbtbmhU-eyJni_C3m5tnnHlQPQJosbR8h5qLDLROg0R7ZVDD5fCtbMDLr-Pvo5t3H5MoX5-QXbPo2WbC35tooDtOv5J5jbjus5p62-KCHtbP8_KL8tD8MbD0Cq6K5j5cWjG4OexneWDTm5-nTtK3VjP_63-jS3pby0M5O2-rLJaKtbM8baU85OCFlD5thD63BeaRKeJQX2COXsJ6VHJOoDDkRjMR5y4LdLp7xJhT00bFf0bRmL-TdO56CbMFMjl4JyM7EtMCeWJLe_KDaJItWbP5kMtn_qttjMfbWetTbHD7yWCv5Wt55OR5JLn7nDpIX0a-fK-7wK66L0lo_2hO1MljhW55SMfJyyGCHt6tjtnAj_Iv55RTWjJuk-4r_bnIJMqJ-2tvtK4o2WbCQJhu28pcNLTDKjbIHLfcaqlkLBK5f-l5-Bt0B8prhjpO1j4_eKG8OttQL3b63blrSt-5J8h5jDh3qb6ksD-RC5JTwJjvy0hvcLR6cShnq5fjrDRLbXU6BK5vPbNcZ0l8K3l02VKO_e6t5jjJLDGtsKbQKaDQ036rh-6rjDnCr2MnOXUI8LNDH2x4HXKTBVlv8LKJbSq54X6rCbbk80RO7ttoAKa535hTR3UjAEf5lqf7nDUL1Db3DW6vMtg3tsRngfInoepvo0tcc3MkF5tjdJJQOBKQB0KnGbUQkeq8CQft205tpeGLfq6tOfnksL6rJbPoEq5rnhPF3-l53KP6-3MJO3b7ZM-tafRjpsh6h5nQRD6_AbbQqKtciLG5AohFLK-oj-D_mD5AB3J; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=28312_1456_21125_28132_28266_22160; delPer=0; PSINO=2; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; locale=zh; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1547433565; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1547433565; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D ',
        'Host': 'fanyi.baidu.com',
        'Origin': 'https: // fanyi.baidu.com',
        'Referer': 'https: // fanyi.baidu.com /?aldtype = 16047'
    }
    trans_url = 'https://fanyi.baidu.com/v2transapi'
    ori_url = 'https://fanyi.baidu.com/'
    content = content
    session = requests.Session()
    token = ''
    gtk = ''

    response = session.get(ori_url, headers=headers)
    html = response.content.decode()
    token_matches = re.findall("token: '(.*?)'", html, re.S)
    for match in token_matches:
        token = match
    gtk_matches = re.findall("window.gtk = '(.*?)';", html, re.S)
    for match in gtk_matches:
        gtk = match

    js = """ 
             var i = null;
                function a(r) {
                    if (Array.isArray(r)) {
                        for (var o = 0, t = Array(r.length); o < r.length; o++)
                            t[o] = r[o];
                        return t
                    }
                    return Array.from(r)
                };

                function n(r, o) {
                    for (var t = 0; t < o.length - 2; t += 3) {
                        var a = o.charAt(t + 2);
                        a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
                        a = "+" === o.charAt(t + 1) ? r >>> a : r << a,
                        r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
                    }
                    return r
                };

                function e(r, gtk) {
                    var t = r.length;
                    t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10));
                    var u = void 0,
                    u = null !== i ? i : (i = gtk || "") || "";
                    for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
                        var A = r.charCodeAt(v);
                        128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)),
                        S[c++] = A >> 18 | 240,
                        S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224,
                        S[c++] = A >> 6 & 63 | 128),
                        S[c++] = 63 & A | 128)
                    }
                    for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++)
                        p += S[b],
                        p = n(p, F);
                    return p = n(p, D),
                    p ^= s,
                    0 > p && (p = (2147483647 & p) + 2147483648),
                    p %= 1e6,
                    p.toString() + "." + (p ^ m)
                };
            """
    sign_function = js2py.EvalJs()
    sign_function.execute(js)
    params = {
        'from': sl,
        'to': tl,
        'query': content,
        'transtype': 'realtime',
        'simple_means_flag': 3,
        'sign': sign_function.e(content, gtk),
        'token': token
    }
    response = session.post(trans_url, headers=headers, data=params)
    data = json.loads(response.content.decode())
    return data['trans_result']['data'][0]['dst'] + '\n(以上内容来自百度翻译)'


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
    ========================================\n
    """
    wx.MessageBox(text, 'Fat Snake Translator --version 2.3', wx.OK | wx.ICON_NONE)


class Window(wx.Frame):
    def __init__(self, parent, title):
        super(Window, self).__init__(parent, title=title, size=(600, 450))

        self.GoogleLanguageDic = {'中文': 'zh-CN', '英文': 'en', '法语': 'fr', '德语': 'de', '葡萄牙语': 'pt', '西班牙语': 'es'}
        self.BaiduLanguageDic = {'英文': 'en', '中文': 'zh', '法语': 'fra', '德语': 'de', '葡萄牙语': 'pt', '西班牙语': 'spa'}

        self.SetMaxSize(size=(600, 415))
        self.SetMinSize(size=(600, 415))
        self.font4label = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName='DengXian')
        self.font4trans = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName='DengXian')
        self.font4btn = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName='DengXian')
        self.font4tfoot = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName='DengXian')

        self.panel = wx.Panel(self)

        self.mode = wx.ToggleButton(self.panel, label='中英互译', pos=(5, 5), size=(60, 25))
        self.Bind(wx.EVT_TOGGLEBUTTON, self.switchMode, self.mode)

        self.label = wx.StaticText(self.panel, label='请 输 入 查 询 内 容：', pos=(220, 5))
        self.label.SetFont(self.font4label)

        self.input = wx.TextCtrl(self.panel, pos=(80, 40), size=(320, 27), style=wx.ALIGN_BOTTOM | wx.TE_PROCESS_ENTER)
        self.input.SetFont(self.font4label)
        self.Bind(wx.EVT_TEXT_ENTER, self.doQuery, self.input)

        self.query = wx.Button(self.panel, pos=(405, 40), label='查询 (回车)', size=(105, 25))
        self.query.SetFont(self.font4btn)
        self.Bind(wx.EVT_BUTTON, self.doQuery, self.query)

        self.clean = wx.Button(self.panel, pos=(405, 70), label='清空', size=(105, 25))
        self.clean.SetFont(self.font4btn)
        self.Bind(wx.EVT_BUTTON, self.cleanText, self.clean)

        '''BAIDU AND GOOGLE'''
        sourceList = list(self.GoogleLanguageDic.keys())
        self.sourceLanguage = wx.ComboBox(self.panel, pos=(80, 72), size=(105, 30), value=sourceList[0],
                                          choices=sourceList,
                                          style=wx.CB_READONLY)
        self.sourceLanguage.Hide()

        targetList = list(self.BaiduLanguageDic.keys())
        self.targetLanguage = wx.ComboBox(self.panel, pos=(200, 72), size=(105, 30), value=targetList[0],
                                          choices=targetList,
                                          style=wx.CB_READONLY)
        self.targetLanguage.Hide()

        self.nameLabel_1 = wx.StaticText(self.panel, pos=(7, 110), label='=================== 百度翻译 '
                                                                         '======================================= 谷歌翻译 '
                                                                         '===================')
        self.nameLabel_1.SetFont(self.font4tfoot)
        self.nameLabel_1.Hide()

        self.baidu = wx.TextCtrl(self.panel, style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_WORDWRAP,
                                 pos=(10, 130),
                                 size=(275, 220))
        self.baidu.Hide()
        self.baidu.SetFont(self.font4trans)

        self.google = wx.TextCtrl(self.panel, style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_WORDWRAP,
                                  pos=(300, 130),
                                  size=(275, 220))
        self.google.Hide()
        self.google.SetFont(self.font4trans)

        '''YOUDAO EN TO CN'''
        self.nameLabel_2 = wx.StaticText(self.panel, pos=(7, 110), label='============================'
                                                                         '=============== 有道翻译 ==============='
                                                                         '============================')
        self.nameLabel_2.SetFont(self.font4tfoot)
        self.youdao = wx.TextCtrl(self.panel, style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_WORDWRAP,
                                  pos=(160, 130),
                                  size=(275, 220))
        self.youdao.SetFont(self.font4trans)

        self.foot = wx.StaticText(self.panel, label='========================================  FAT SNAKE  2.4  '
                                                    '========================================', pos=(7, 355))
        self.foot.SetFont(self.font4tfoot)

        self.logButton = wx.Button(self.panel, label='log', pos=(545, 5), size=(35, 25))
        self.Bind(wx.EVT_BUTTON, versionInfo, self.logButton)

        self.Centre()
        self.Show()
        self.Fit()

    def cleanText(self, event):
        self.input.SetLabelText('')
        self.youdao.SetLabelText('')
        self.google.SetLabelText('')
        self.baidu.SetLabelText('')

    def doQuery(self, event):
        query = self.input.GetValue()
        if query != '':
            if not self.mode.GetValue():
                resYoudao = getResultYoudao(query)
                self.youdao.SetValue(resYoudao)
            else:
                sL = self.sourceLanguage.GetValue()
                tL = self.targetLanguage.GetValue()
                if sL == tL:
                    wx.MessageBox('请设置不同的输入语言和输出语言！', '提示！', wx.OK | wx.ICON_INFORMATION)
                else:
                    # baidiSL = self.BaiduLanguageDic[self.sourceLanguage.GetValue()]
                    # baidiTL = self.BaiduLanguageDic[self.targetLanguage.GetValue()]
                    googleSL = self.GoogleLanguageDic[self.sourceLanguage.GetValue()]
                    googleTL = self.GoogleLanguageDic[self.targetLanguage.GetValue()]

                    # resBaidu = getResultBaidu(query, baidiSL, baidiTL)
                    resGoogle = getResultGoogle(query, googleSL, googleTL)
                    # self.baidu.SetValue(resBaidu)
                    self.google.SetValue(resGoogle)
        else:
            wx.MessageBox('输入内容为空！\n请重新输入！', '提示！', wx.OK | wx.ICON_INFORMATION)

    def switchMode(self, event):
        self.cleanText(self)
        if not self.mode.GetValue():
            self.mode.SetLabelText('中英互译')
            self.sourceLanguage.Hide()
            self.targetLanguage.Hide()
            self.nameLabel_1.Hide()
            self.baidu.Hide()
            self.google.Hide()

            self.nameLabel_2.Show()
            self.youdao.Show()
        else:
            self.nameLabel_2.Hide()
            self.youdao.Hide()

            self.mode.SetLabelText('多语互译')
            self.sourceLanguage.Show()
            self.targetLanguage.Show()
            self.nameLabel_1.Show()
            self.baidu.Show()
            self.google.Show()


if __name__ == '__main__':
    app = wx.App()
    Window(None, '肥蛇翻译 2.4')
    app.MainLoop()
