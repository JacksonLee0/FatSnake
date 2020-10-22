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
FAT SNAKE 2.5
肥蛇翻译2.5版本更新日志
1. 移除多语互译中的百度翻译，因为百度翻译太垃圾了，谷歌翻译足以。
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
    --- 重新调整界面，翻译显示区域增大。\n
    ========================================\n
    """
    wx.MessageBox(text, 'Fat Snake Translator --version 2.5', wx.OK | wx.ICON_NONE)


class Window(wx.Frame):
    def __init__(self, parent, title):
        super(Window, self).__init__(parent, title=title, size=(500, 450))

        self.GoogleLanguageDic = {'中文': 'zh-CN', '英文': 'en', '法语': 'fr', '德语': 'de', '葡萄牙语': 'pt', '西班牙语': 'es',
                                  '意大利语': 'it', '韩语': 'ko', '日语': 'ja', '俄语': 'ru'}

        self.SetMaxSize(size=(500, 450))
        self.SetMinSize(size=(500, 450))
        self.font4label = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName='DengXian')
        self.font4trans = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName='DengXian')
        self.font4btn = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName='DengXian')
        self.font4tfoot = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName='DengXian')

        self.panel = wx.Panel(self)

        self.mode = wx.ToggleButton(self.panel, label='中英互译', pos=(5, 5), size=(60, 25))
        self.Bind(wx.EVT_TOGGLEBUTTON, self.switchMode, self.mode)

        self.label = wx.StaticText(self.panel, label='请 输 入 查 询 内 容：', pos=(170, 10))
        self.label.SetFont(self.font4label)

        self.input = wx.TextCtrl(self.panel, pos=(80, 40), size=(320, 27), style=wx.ALIGN_BOTTOM | wx.TE_PROCESS_ENTER)
        self.input.SetFont(self.font4label)
        self.Bind(wx.EVT_TEXT_ENTER, self.doQuery, self.input)

        self.query = wx.Button(self.panel, pos=(119, 75), label='查询 (回车)', size=(112, 25))
        self.query.SetFont(self.font4btn)
        self.Bind(wx.EVT_BUTTON, self.doQuery, self.query)

        self.clean = wx.Button(self.panel, pos=(249, 75), label='清空', size=(112, 25))
        self.clean.SetFont(self.font4btn)
        self.Bind(wx.EVT_BUTTON, self.cleanText, self.clean)

        '''GOOGLE'''
        sourceList = list(self.GoogleLanguageDic.keys())
        self.sourceLanguage = wx.ComboBox(self.panel, pos=(120, 105), size=(110, 30), value=sourceList[0],
                                          choices=sourceList,
                                          style=wx.CB_READONLY)
        self.sourceLanguage.Hide()

        targetList = list(self.GoogleLanguageDic.keys())
        self.targetLanguage = wx.ComboBox(self.panel, pos=(250, 105), size=(110, 30), value=targetList[0],
                                          choices=targetList,
                                          style=wx.CB_READONLY)
        self.targetLanguage.Hide()

        self.nameLabel_1 = wx.StaticText(self.panel, pos=(5, 140), label='===================='
                                                                         '=============== 谷歌翻译 ==============='
                                                                         '====================')
        self.nameLabel_1.SetFont(self.font4tfoot)
        self.nameLabel_1.Hide()

        self.trans = wx.TextCtrl(self.panel, style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_WORDWRAP,
                                 pos=(20, 160), size=(445, 230))
        self.trans.SetFont(self.font4trans)

        '''YOUDAO EN TO CN'''
        self.nameLabel_2 = wx.StaticText(self.panel, pos=(5, 140), label='===================='
                                                                         '=============== 有道翻译 ==============='
                                                                         '====================')
        self.nameLabel_2.SetFont(self.font4tfoot)

        self.foot = wx.StaticText(self.panel, label='================================  FAT SNAKE  2.5  '
                                                    '================================', pos=(5, 395))
        self.foot.SetFont(self.font4tfoot)

        self.logButton = wx.Button(self.panel, label='log', pos=(445, 5), size=(35, 25))
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
                resYoudao = getResultYoudao(query)
                self.trans.SetValue(resYoudao)
            else:
                sL = self.sourceLanguage.GetValue()
                tL = self.targetLanguage.GetValue()
                if sL == tL:
                    wx.MessageBox('请设置不同的输入语言和输出语言！', '提示！', wx.OK | wx.ICON_INFORMATION)
                else:
                    googleSL = self.GoogleLanguageDic[self.sourceLanguage.GetValue()]
                    googleTL = self.GoogleLanguageDic[self.targetLanguage.GetValue()]
                    resGoogle = getResultGoogle(query, googleSL, googleTL)
                    self.trans.SetValue(resGoogle)
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
        else:
            self.nameLabel_2.Hide()
            self.mode.SetLabelText('多语互译')
            self.sourceLanguage.Show()
            self.targetLanguage.Show()
            self.nameLabel_1.Show()


if __name__ == '__main__':
    app = wx.App()
    Window(None, '肥蛇翻译 2.5')
    app.MainLoop()
