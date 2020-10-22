#!/usr/bin/python
# -*- coding: UTF-8 -*
# -
import re
import urllib

import js2py
import requests
import wx
from bs4 import BeautifulSoup

"""
"""
"""
FAT SNAKE 2.3
肥蛇翻译2.3版本更新日志
1. 改用wxpython控件,用于修复中文输入法下输入y会卡顿的bug ok
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
    except AttributeError as e:
        wx.MessageBox('输入内容有误！\n请重新输入！', '提示！', wx.OK | wx.ICON_ERROR)
    finally:
        return final_text


""" GOOGLE TRANSLATOR """


def getResultGoogle(target):
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
        model = re.compile(u'[\u4e00-\u9fa5]')

        if model.search(target):
            tl = 'en'
        else:
            tl = 'zh-CN'

        param = {'tk': token(target), 'q': target, 'tl': tl}
        result = requests.get("http://translate.google.cn/translate_a/single?client=t&sl=auto&"
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
    ====================\n
    2.0 版本更新日志:\n
    --- 改名为肥蛇翻译，在这个世界上应该找不到比我的翻译器更帅的名字。\n
    2.1 版本更新日志\n
    --- 新增谷歌翻译英转中。\n
    2.2 版本更新日志：\n
    --- 加入回车键查询单词。\n
    --- 支持有道翻译中英互译。\n
    --- 修复谷歌翻译中转英互译乱码bug。\n
    2.3 版本更新日志:\n
    --- 修复中文输入法下，输入y的单词卡顿问题。\n
    --- 小幅升级用户界面。\n
    ====================
    """
    wx.MessageBox(text, 'Fat Snake Translator --version 2.3', wx.OK | wx.ICON_NONE)


class Window(wx.Frame):
    def __init__(self, parent, title):
        super(Window, self).__init__(parent, title=title, size=(600, 400))

        self.SetMaxSize(size=(600, 400))
        self.SetMinSize(size=(600, 400))
        self.font4label = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.font4trans = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.font4tfoot = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        self.panel = wx.Panel(self)

        self.label = wx.StaticText(self.panel, label='请 输 入 查 询 内 容：', pos=(220, 5))
        self.label.SetFont(self.font4label)

        self.input = wx.TextCtrl(self.panel, pos=(100, 30), size=(400, 25), style=wx.ALIGN_LEFT | wx.TE_PROCESS_ENTER)
        self.input.SetFont(self.font4trans)
        self.Bind(wx.EVT_TEXT_ENTER, self.doQuery, self.input)

        self.query = wx.Button(self.panel, pos=(140, 60), label='查询 (回车)', size=(130, 26))
        self.query.SetFont(self.font4trans)
        self.Bind(wx.EVT_BUTTON, self.doQuery, self.query)

        self.clean = wx.Button(self.panel, pos=(320, 60), label='清空', size=(130, 26))
        self.clean.SetFont(self.font4trans)
        self.Bind(wx.EVT_BUTTON, self.cleanText, self.clean)

        self.nameLabel = wx.StaticText(self.panel, pos=(7, 100), label='=================== 有道翻译 '
                                                                       '======================================= 谷歌翻译 '
                                                                       '===================')
        self.nameLabel.SetFont(self.font4tfoot)

        self.youdao = wx.TextCtrl(self.panel, style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_WORDWRAP,
                                  pos=(10, 120),
                                  size=(275, 220))
        self.youdao.SetFont(self.font4trans)

        self.google = wx.TextCtrl(self.panel, style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_WORDWRAP,
                                  pos=(300, 120),
                                  size=(275, 220))
        self.google.SetFont(self.font4trans)

        self.foot = wx.StaticText(self.panel, label='========================================  FAT SNAKE  2.3  '
                                                    '========================================', pos=(7, 345))
        self.foot.SetFont(self.font4tfoot)

        pic = wx.Image('C:\\Users\\Dongming\\PycharmProjects\\python3-selfstudy\\FatSnake\\info.ico',
                       wx.BITMAP_TYPE_ICO).ConvertToBitmap()
        self.infoButton = wx.BitmapButton(self.panel, bitmap=pic, pos=(550, 5), size=(30, 30))
        self.Bind(wx.EVT_BUTTON, versionInfo, self.infoButton)

        self.Centre()
        self.Show()
        self.Fit()

    def cleanText(self, event):
        self.input.SetLabelText('')
        self.youdao.SetLabelText('')
        self.google.SetLabelText('')

    def doQuery(self, event):
        query = self.input.GetValue()
        if query != '':
            resYoudao = getResultYoudao(query)
            if resYoudao:
                resGoogle = getResultGoogle(query)
                self.youdao.SetValue(resYoudao)
                self.google.SetValue(resGoogle)
        else:
            wx.MessageBox('输入内容为空！\n请重新输入！', '提示！', wx.OK | wx.ICON_INFORMATION)


if __name__ == '__main__':
    app = wx.App()
    Window(None, '肥蛇翻译 2.3')
    app.MainLoop()
