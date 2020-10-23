#!/usr/bin/python
# -*- coding: UTF-8 -*
# -
import hashlib
import json
import re

import pymongo
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
3.0
"""
"""
"""
version_number = '3.0'

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
                final_text += '(无翻译结果)\n'

            return final_text
        except AttributeError as e:
            wx.MessageBox('输入内容有误！\n请重新输入！', '提示！', wx.OK | wx.ICON_ERROR)
            return final_text
    except requests.exceptions.RequestException as e:
        wx.MessageBox('有道服务器连接出现故障！\n这是垃圾有道的问题！不是程序的问题！\n请重试或者用谷歌翻译试试！', '提示', wx.OK | wx.ICON_ERROR)
        return final_text


def getLongTranslationYoudao(content: 'str'):
    timestamp = time.time()
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
    2.8 版本更新日志:\n
    --- 完善界面，现在可以自由调整翻译器窗口大小。\n
    2.9 -- final offline version 版本更新日志:\n
    --- 新增设置窗口，可以调整翻译文本字体大小。\n
    2.9 -- final offline version.1 版本更新日志：\n
    --- 由于垃圾有道翻译时不时会血崩，故增加了响应判断窗口，以防翻译器崩溃。\n
    3.0 版本更新日志：\n
    --- 新增复制按钮，一键复制翻译内容。\n
    --- 新增用户模式，注册账号登录后可查看翻译你的肥蛇生涯数据。\n
    ========================================\n
    """
    wx.MessageBox(text, 'Fat Snake Translator --version ' + version_number, wx.OK | wx.ICON_NONE)


class Window(wx.Frame):
    def __init__(self, parent, title):
        super(Window, self).__init__(parent, title=title, size=(605, 420))

        self.GoogleLanguageDic = {'中文': 'zh-CN', '英文': 'en', '法语': 'fr', '德语': 'de', '葡萄牙语': 'pt', '西班牙语': 'es',
                                  '意大利语': 'it', '韩语': 'ko', '日语': 'ja', '俄语': 'ru'}
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
        self.accountInformation = [False, '', 0, 0]

        self.mode = wx.ToggleButton(self.panel, label='中英互译', pos=(5, 5), size=(60, 25))
        self.Bind(wx.EVT_TOGGLEBUTTON, self.switchMode, self.mode)

        self.label_1 = wx.StaticText(self.panel, label='请输入查询内容：', pos=(10, 52))
        self.label_1.SetFont(self.font4label)

        self.label_2 = wx.StaticText(self.panel, label='查询结果：')
        self.label_2.SetFont(self.font4label)

        self.input = wx.TextCtrl(self.panel, pos=(10, 105), size=(280, 250), style=wx.TE_MULTILINE | wx.TE_WORDWRAP, )
        self.input.SetFont(self.font4label)
        self.Bind(wx.EVT_TEXT_ENTER, self.doQuery, self.input)  # 回车查询

        self.trans = wx.TextCtrl(self.panel, style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_WORDWRAP | wx.EXPAND,
                                 pos=(300, 105), size=(280, 250))
        self.trans.SetFont(self.font4label)

        self.query = wx.Button(self.panel, label='查询 (回车)', size=(112, 25), style=wx.NO_BORDER)
        self.query.SetFont(self.font4btn)
        self.Bind(wx.EVT_BUTTON, self.doQuery, self.query)

        self.clean = wx.Button(self.panel, label='清空', size=(55, 25))
        self.clean.SetFont(self.font4btn)
        self.Bind(wx.EVT_BUTTON, self.cleanText, self.clean)

        self.copyButton = wx.Button(self.panel, label='复制', size=(55, 25))
        self.copyButton.SetFont(self.font4btn)
        self.Bind(wx.EVT_BUTTON, self.copyText, self.copyButton)

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

        self.nameLabel_1 = wx.StaticText(self.panel, pos=(9, 33), label='谷歌翻译 ' + '=' * 350)
        self.nameLabel_1.SetFont(self.font4tfoot)
        self.nameLabel_1.Hide()

        self.switch = wx.Button(self.panel, size=(39, 25), label='交换')
        self.Bind(wx.EVT_BUTTON, self.switchText, self.switch)
        self.switch.Hide()

        self.resList = []
        '''GOOGLE ELEMENT'''

        '''YOUDAO ELEMENT'''
        self.nameLabel_2 = wx.StaticText(self.panel, pos=(9, 33), label='有道翻译 ' + '=' * 350)
        self.nameLabel_2.SetFont(self.font4tfoot)

        self.foot = wx.StaticText(self.panel,
                                  label='FAT SNAKE ' + version_number + ' ' + '=' * 350)
        self.foot.SetFont(self.font4tfoot)
        '''YOUDAO ELEMENT'''

        self.loginButton = wx.Button(self.panel, label='用户', size=(35, 25))
        self.Bind(wx.EVT_BUTTON, self.accountInterface, self.loginButton)

        self.settingButton = wx.Button(self.panel, label='设置', size=(35, 25))
        self.Bind(wx.EVT_BUTTON, self.OnSetting, self.settingButton)

        self.Centre()
        self.Show()
        self.Fit()

    def cleanText(self, event):
        self.input.SetLabelText('')
        self.trans.SetLabelText('')

    def copyText(self, event):
        text_obj = wx.TextDataObject()
        text_obj.SetText(self.trans.GetValue())
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
            wx.TheClipboard.SetData(text_obj)
            wx.TheClipboard.Close()

    def doQuery(self, event):
        query = self.input.GetValue().lstrip('\n').rstrip('\n')
        if query != '':
            if not self.mode.GetValue():
                resYoudao = getResultYoudao(query) if len(query) < 10 else getLongTranslationYoudao(query)
                self.trans.SetValue(resYoudao)
                userName = self.accountInformation[1] if self.accountInformation[0] else 'None'
                translatedInfo.insert_one(
                    {'_id': time.strftime("%Y-%m-%d %H:%M:%S"), "originalText": query, "translatedText": resYoudao,
                     'userName': userName})
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
                    userName = self.accountInformation[1] if self.accountInformation[0] else 'None'
                    translatedInfo.insert_one(
                        {'_id': time.strftime("%Y-%m-%d %H:%M:%S"), "originalText": query, "translatedText": resGoogle,
                         'userName': userName})

            if self.accountInformation[0]:
                condition = {'_id': self.accountInformation[1]}
                user = userInfo.find_one(condition)
                previousNum = user['totalTranslatedLength']
                zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
                if zhPattern.search(query):
                    length = len(query)
                else:
                    length = len(query.split())
                user['totalTranslatedLength'] = previousNum + length
                userInfo.update_one(condition, {'$set': user})

                self.accountInformation[2] += length
                self.accountInformation[3] += length
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
        else:
            self.sourceLanguage.SetValue(TranslatedLanguage)
            self.targetLanguage.SetValue(OriginalLanguage)

    def OnSize(self, event):
        # Adaptive position
        self.x = event.GetSize().x
        self.y = event.GetSize().y
        self.foot.SetPosition((9, self.y - 17))
        self.loginButton.SetPosition((self.x - 80, 5))
        self.settingButton.SetPosition((self.x - 39, 5))
        self.label_2.SetPosition((self.x / 2 + 5, 52))
        self.query.SetPosition((self.x / 2 - 124, 50))
        self.clean.SetPosition((self.x - 129, 50))
        self.copyButton.SetPosition((self.x - 72, 50))
        self.trans.SetPosition((self.x / 2 + 5, 105))
        self.sourceLanguage.SetPosition((self.x / 2 - 123, 77))
        self.targetLanguage.SetPosition((self.x - 128, 77))
        self.switch.SetPosition((self.x / 2 + 10, 76))

        # Adaptive Textbox size
        self.input.SetSize((self.x / 2 - 15, self.y - 125))
        self.trans.SetSize((self.x / 2 - 15, self.y - 125))

    def OnSetting(self, event):
        self.settingDialog = DialogSetting(self, '设置', self.font4trans.GetPointSize())
        self.settingDialog.Bind(wx.EVT_CLOSE, self.setFontSize)
        self.settingDialog.ShowWindowModal()

    def setFontSize(self, event):
        self.font4trans.SetPointSize(self.settingDialog.getFontSize(self))
        self.input.SetFont(self.font4trans)
        self.trans.SetFont(self.font4trans)
        self.settingDialog.Destroy()

    def accountInterface(self, event):
        self.accountDialog = DialogAccount(self, '用户窗口', self.accountInformation)
        self.accountDialog.Bind(wx.EVT_CLOSE, self.getAllStatus)
        self.accountDialog.ShowWindowModal()

    def getAllStatus(self, event):
        self.accountInformation = self.accountDialog.getAllStatus(self)
        self.accountDialog.Destroy()


class DialogSetting(wx.Dialog):
    def __init__(self, parent, title, fontSize):
        super(DialogSetting, self).__init__(parent, title=title, size=(250, 170))
        panelDialogSetting = wx.Panel(self)
        self.fontSizeDic = {'10': '小', '11': '中', '12': '大', '15': '超大', '17': '超级无敌猪皮大'}
        fontSizeList = list(self.fontSizeDic.values())
        self.fontLabel = wx.StaticText(panelDialogSetting, label='字体大小：', pos=(20, 43))
        self.transFontSize = wx.ComboBox(panelDialogSetting, size=(110, 30), pos=(100, 40),
                                         value=self.fontSizeDic[str(fontSize)],
                                         choices=fontSizeList,
                                         style=wx.TE_READONLY)
        self.logButton = wx.Button(panelDialogSetting, label='日志', size=(40, 25), pos=(190, 5))
        self.Bind(wx.EVT_BUTTON, versionInfo, self.logButton)
        self.Center()

    def getFontSize(self, event):
        return int(list(self.fontSizeDic.keys())[list(self.fontSizeDic.values()).index(self.transFontSize.GetValue())])


class DialogAccount(wx.Dialog):
    def __init__(self, parent, title, accountInformation):
        super(DialogAccount, self).__init__(parent, title=title, size=(300, 200))
        self.accountInformation = accountInformation
        self.panelDialogAccount = wx.Panel(self)

        self.userNameLabel = wx.StaticText(self.panelDialogAccount, pos=(30, 30), label='用户名：')
        self.passwordLabel = wx.StaticText(self.panelDialogAccount, pos=(30, 60), label='密码：')

        self.userNameInput = wx.TextCtrl(self.panelDialogAccount, pos=(100, 30), size=(150, 22))
        self.passwordInput = wx.TextCtrl(self.panelDialogAccount, pos=(100, 60), size=(150, 22), style=wx.TE_PASSWORD)

        self.LogInButton = wx.Button(self.panelDialogAccount, label='登录', pos=(60, 120), size=(60, 25))
        self.SignUpButton = wx.Button(self.panelDialogAccount, label='注册', pos=(160, 120), size=(60, 25))

        self.Bind(wx.EVT_BUTTON, self.checkLogIn, self.LogInButton)
        self.Bind(wx.EVT_BUTTON, self.checkSignUp, self.SignUpButton)

        self.userName = wx.StaticText(self.panelDialogAccount, label=accountInformation[1], pos=(100, 30))
        self.TransLengthLabel = wx.StaticText(self.panelDialogAccount, label='本次使用查询单词数：', pos=(30, 60))
        self.TransLength = wx.StaticText(self.panelDialogAccount, label=str(accountInformation[2]), pos=(180, 60))
        self.TransLengthTotalLabel = wx.StaticText(self.panelDialogAccount, label='用户查询单词总数：', pos=(30, 90))
        self.TransLengthTotal = wx.StaticText(self.panelDialogAccount, label=str(accountInformation[3]), pos=(180, 90))

        self.LogOutButton = wx.Button(self.panelDialogAccount, label='退出登录', pos=(100, 120), size=(80, 25))
        self.Bind(wx.EVT_BUTTON, self.checkLogOut, self.LogOutButton)

        if accountInformation[0] is False:
            self.userName.Hide()
            self.LogOutButton.Hide()
            self.TransLengthLabel.Hide()
            self.TransLength.Hide()
            self.TransLengthTotal.Hide()
            self.TransLengthTotalLabel.Hide()
        else:
            self.passwordLabel.Hide()
            self.userNameInput.Hide()
            self.passwordInput.Hide()
            self.LogInButton.Hide()
            self.SignUpButton.Hide()

        self.Center()

    def checkLogIn(self, event):
        if not self.accountInformation[0]:
            if self.userNameInput.GetValue() == '' or self.passwordInput.GetValue() == '':
                wx.MessageBox('用户名或密码不能为空！\n请输入正确的用户名和密码！', '提示！', wx.OK | wx.ICON_INFORMATION)
            elif userInfo.find_one({'_id': self.userNameInput.GetValue()}) is None:
                wx.MessageBox('用户名不存在，请注册！', '提示！', wx.OK | wx.ICON_INFORMATION)
            elif userInfo.find_one({'_id': self.userNameInput.GetValue(), 'password': self.passwordInput.GetValue()}):
                wx.MessageBox('登录成功！', '提示！', wx.OK | wx.ICON_INFORMATION)
                self.logInSuccess(self)
            else:
                wx.MessageBox('密码错误！请重新输入！', '提示！', wx.OK | wx.ICON_INFORMATION)
        else:
            pass

    def checkSignUp(self, event):
        if self.userNameInput.GetValue() == '' or self.passwordInput.GetValue() == '':
            wx.MessageBox('注册用户名或密码不能为空！\n请输入正确的用户名和密码！', '提示！', wx.OK | wx.ICON_INFORMATION)

        elif len(self.userNameInput.GetValue()) < 6 or len(self.userNameInput.GetValue()) > 12:
            wx.MessageBox('用户名长度为6-12位！\n请输入对应长度的用户名！', '提示！', wx.OK | wx.ICON_INFORMATION)

        elif not self.passwordInput.GetValue().isalnum() or len(self.passwordInput.GetValue()) < 8:
            wx.MessageBox('密码应包含字母和数字！\n密码长度至少为8位！\n请输入正确格式的密码！', '提示！', wx.OK | wx.ICON_INFORMATION)

        elif userInfo.find_one({'_id': self.userNameInput.GetValue()}):
            wx.MessageBox('用户名已注册！请登录！', '提示！', wx.OK | wx.ICON_INFORMATION)
        else:
            userInfo.insert_one({'_id': self.userNameInput.GetValue(), 'password': self.passwordInput.GetValue(),
                                 'totalTranslatedLength': 0})
            wx.MessageBox('注册成功！请登录！', '提示！', wx.OK | wx.ICON_INFORMATION)

    def checkLogOut(self, event):
        self.accountInformation = [False, '', 0, 0]
        self.userName.SetLabel('')

        self.passwordLabel.Show()
        self.userNameInput.Show()
        self.passwordInput.Show()
        self.LogInButton.Show()
        self.SignUpButton.Show()

        self.userName.Hide()
        self.LogOutButton.Hide()
        self.TransLengthLabel.Hide()
        self.TransLength.Hide()
        self.TransLengthTotal.Hide()
        self.TransLengthTotalLabel.Hide()

    def logInSuccess(self, event):
        self.passwordLabel.Hide()
        self.userNameInput.Hide()
        self.passwordInput.Hide()
        self.LogInButton.Hide()
        self.SignUpButton.Hide()

        self.userName.SetLabel(self.userNameInput.GetValue())

        self.accountInformation[0] = True
        self.accountInformation[1] = self.userName.GetLabel()
        self.accountInformation[2] = 0
        temp = userInfo.find_one({'_id': self.userName.GetLabel()})
        length = temp['totalTranslatedLength']
        self.accountInformation[3] = length
        self.TransLengthTotal.SetLabel(str(length))
        self.userName.Show()
        self.LogOutButton.Show()
        self.TransLengthLabel.Show()
        self.TransLength.Show()
        self.TransLengthTotal.Show()
        self.TransLengthTotalLabel.Show()

        self.userNameInput.SetLabel('')
        self.passwordInput.SetLabel('')

    def getAllStatus(self, event):
        return self.accountInformation


if __name__ == '__main__':
    url = "mongodb://dongming-asia-2:jDMRV6fwHXcVNNBw7bLonz7e9OXgPPeFHOOc7EbCAdEJJvOj4nIxW9FKaV2Bb1xc9hFl0dc8eOP6TsikGvFwxQ==@dongming-asia-2.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
    client = pymongo.MongoClient(url)
    db = client.fatsnake
    translatedInfo = db.translatedInfo
    userInfo = db.userInfo

    app = wx.App()
    Window(None, '肥蛇翻译 ' + version_number)
    app.MainLoop()
