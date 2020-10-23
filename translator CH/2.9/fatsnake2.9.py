#!/usr/bin/python
# -*- coding: UTF-8 -*
# -
import hashlib
import json
import random
import time
import urllib
from urllib import parse

import js2py
import requests
import wx
from bs4 import BeautifulSoup

"""
"""
"""
FAT SNAKE 2.9 
"""
"""
"""
version_number = '2.9'

""" YOUDAO TRANSLATOR"""


def getResultYoudao(content: 'str'):
    url = 'http://www.youdao.com/w/' + urllib.parse.quote(content.lstrip()) + '/#keyfrom=dict2.top'
    final_text = ''
    try:
        req = requests.get(url=url, timeout=1.5)
        bf = BeautifulSoup(req.text, features="html.parser")
        body = bf.body
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
                        final_text += (span.get_text().replace('\n', '').strip()) + '\n'

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
    except requests.exceptions.RequestException as e:
        wx.MessageBox('Connection Error!\nTry again or use Google Translate!', 'Message', wx.OK | wx.ICON_ERROR)
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
        allText[1] += '\n(The above content comes from Google Translate)\n'
        if list(result.json())[1] is not None:
            text = list(result.json())[1]
            for element in text:
                allText[2] += element[0] + '.\n'
                allText[2] += '；'.join(element[1]) + '\n'
            allText[3] += '(The above content comes from Google Dictionary)'
        return allText


""" INTERFACE """


def versionInfo(event):
    text = """
    ========================================\n
    To be updated...
    ========================================\n
    """
    wx.MessageBox(text, 'Fat Snake Translator --version ' + version_number, wx.OK | wx.ICON_NONE)


class Window(wx.Frame):
    def __init__(self, parent, title):
        super(Window, self).__init__(parent, title=title, size=(605, 420))

        self.GoogleLanguageDic = {'Chinese': 'zh-CN', 'English': 'en', 'French': 'fr', 'German': 'de',
                                  'Portuguese': 'pt', 'Spanish': 'es',
                                  'Italian': 'it', 'Korean': 'ko', 'Japanese': 'ja', 'Russian': 'ru'}
        self.SetMinSize(size=(605, 420))
        self.font4label = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName='DengXian')
        self.font4trans = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName='DengXian')

        self.font4btn = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName='DengXian')
        self.font4tfoot = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName='DengXian')

        self.x = 0
        self.y = 0
        self.panel = wx.Panel(self)
        self.panel.Bind(wx.EVT_SIZE, self.OnSize)

        '''MAIN ELEMENT'''
        self.mode = wx.ToggleButton(self.panel, label='CH-EN', pos=(5, 5), size=(70, 25))
        self.Bind(wx.EVT_TOGGLEBUTTON, self.switchMode, self.mode)

        self.settingButton = wx.Button(self.panel, label='Setting', size=(100, 25))
        self.Bind(wx.EVT_BUTTON, self.OnSetting, self.settingButton)

        self.label_1 = wx.StaticText(self.panel, label='Please enter your\nquery below:', pos=(10, 52))

        self.label_2 = wx.StaticText(self.panel, label='Result:')

        self.input = wx.TextCtrl(self.panel, pos=(10, 105), size=(280, 250), style=wx.TE_MULTILINE | wx.TE_WORDWRAP, )
        self.input.SetFont(self.font4label)
        self.Bind(wx.EVT_TEXT_ENTER, self.doQuery, self.input)

        self.trans = wx.TextCtrl(self.panel, style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_WORDWRAP | wx.EXPAND,
                                 pos=(300, 105), size=(280, 250))
        self.trans.SetFont(self.font4label)

        self.query = wx.Button(self.panel, label='Query', size=(112, 25), style=wx.NO_BORDER)
        self.Bind(wx.EVT_BUTTON, self.doQuery, self.query)

        self.clean = wx.Button(self.panel, label='clear', size=(112, 25))
        self.Bind(wx.EVT_BUTTON, self.cleanText, self.clean)
        '''MAIN ELEMENT'''

        '''GOOGLE ELEMENT'''
        sourceList = list(self.GoogleLanguageDic.keys())
        self.sourceLanguage = wx.ComboBox(self.panel, size=(110, 30), value=sourceList[1],
                                          choices=sourceList,
                                          style=wx.TE_READONLY)
        self.sourceLanguage.Hide()

        targetList = list(self.GoogleLanguageDic.keys())
        self.targetLanguage = wx.ComboBox(self.panel, size=(110, 30), value=targetList[0],
                                          choices=targetList,
                                          style=wx.TE_READONLY)
        self.targetLanguage.Hide()

        self.nameLabel_1 = wx.StaticText(self.panel, pos=(9, 33), label='Google' + '=' * 350)
        self.nameLabel_1.SetFont(self.font4tfoot)
        self.nameLabel_1.Hide()

        self.switch = wx.Button(self.panel, size=(39, 25), label='Swap')
        self.Bind(wx.EVT_BUTTON, self.switchText, self.switch)
        self.switch.Hide()

        self.resList = []
        '''GOOGLE ELEMENT'''

        '''YOUDAO ELEMENT'''
        self.nameLabel_2 = wx.StaticText(self.panel, pos=(9, 33), label='Youdao ' + '=' * 350)
        self.nameLabel_2.SetFont(self.font4tfoot)

        self.foot = wx.StaticText(self.panel,
                                  label='FAT SNAKE ' + version_number + ' ' + '=' * 350)
        self.foot.SetFont(self.font4tfoot)
        '''YOUDAO ELEMENT'''

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
                if len(query) < 10:
                    resYoudao = getResultYoudao(query)
                else:
                    resYoudao = getLongTranslationYoudao(query)
                self.trans.SetValue(resYoudao)
            else:
                sL = self.sourceLanguage.GetValue()
                tL = self.targetLanguage.GetValue()
                if sL == tL:
                    wx.MessageBox('Please set a different input language and output language!', 'Message!',
                                  wx.OK | wx.ICON_INFORMATION)
                else:
                    googleSL = self.GoogleLanguageDic[self.sourceLanguage.GetValue()]
                    googleTL = self.GoogleLanguageDic[self.targetLanguage.GetValue()]
                    self.resList = getResultGoogle(query, googleSL, googleTL)
                    resGoogle = ''.join(map(str, self.resList))
                    self.trans.SetValue(resGoogle)
        else:
            wx.MessageBox('Input is empty!\nPlease try again!', 'Message!', wx.OK | wx.ICON_INFORMATION)

    def switchMode(self, event):
        self.cleanText(self)
        if not self.mode.GetValue():
            self.mode.SetLabelText('CH-EN')
            self.sourceLanguage.Hide()
            self.targetLanguage.Hide()
            self.nameLabel_1.Hide()
            self.nameLabel_2.Show()
            self.switch.Hide()
        else:
            self.nameLabel_2.Hide()
            self.mode.SetLabelText('All')
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
        else:
            self.sourceLanguage.SetValue(TranslatedLanguage)
            self.targetLanguage.SetValue(OriginalLanguage)

    def OnSize(self, event):
        # Adaptive position
        self.x = event.GetSize().x
        self.y = event.GetSize().y
        self.foot.SetPosition((9, self.y - 17))
        self.settingButton.SetPosition((self.x - 105, 5))
        self.label_2.SetPosition((self.x / 2 + 5, 52))
        self.query.SetPosition((self.x / 2 - 124, 50))
        self.clean.SetPosition((self.x - 129, 50))
        self.trans.SetPosition((self.x / 2 + 5, 105))
        self.sourceLanguage.SetPosition((self.x / 2 - 123, 77))
        self.targetLanguage.SetPosition((self.x - 128, 77))
        self.switch.SetPosition((self.x / 2 + 10, 76))

        # Adaptive Textbox size
        self.input.SetSize((self.x / 2 - 15, self.y - 125))
        self.trans.SetSize((self.x / 2 - 15, self.y - 125))

    def OnSetting(self, event):
        self.settingDialog = Dialog(self, 'Setting', self.font4trans.GetPointSize())
        self.settingDialog.Bind(wx.EVT_CLOSE, self.setFontSize)
        self.settingDialog.ShowWindowModal()

    def setFontSize(self, event):
        self.font4trans.SetPointSize(self.settingDialog.getFontSize(self))
        self.input.SetFont(self.font4trans)
        self.trans.SetFont(self.font4trans)
        self.settingDialog.Destroy()


class Dialog(wx.Dialog):
    def __init__(self, parent, title, fontSize):
        super(Dialog, self).__init__(parent, title=title, size=(250, 170))
        panelDialog = wx.Panel(self)
        self.fontSizeDic = {'10': 'Small', '11': 'Medium', '12': 'Big', '15': 'Super Big', '17': 'Extremely Big'}
        fontSizeList = list(self.fontSizeDic.values())
        self.fontLabel = wx.StaticText(panelDialog, label='Font size:', pos=(20, 43))
        self.transFontSize = wx.ComboBox(panelDialog, size=(110, 30), pos=(100, 40),
                                         value=self.fontSizeDic[str(fontSize)],
                                         choices=fontSizeList,
                                         style=wx.TE_READONLY)
        self.logButton = wx.Button(panelDialog, label='Log', size=(40, 25), pos=(190, 5))
        self.Bind(wx.EVT_BUTTON, versionInfo, self.logButton)
        self.Center()

    def getFontSize(self, event):
        return int(list(self.fontSizeDic.keys())[list(self.fontSizeDic.values()).index(self.transFontSize.GetValue())])


if __name__ == '__main__':
    app = wx.App()
    Window(None, 'FatSnake Translator ' + version_number)
    app.MainLoop()
