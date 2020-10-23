#!/usr/bin/python
# -*- coding: UTF-8 -*
# -
import re
import tkinter
import urllib
from tkinter import messagebox
from tkinter import scrolledtext

import js2py
import requests
from bs4 import BeautifulSoup

"""
FAT SNAKE 2.2
肥蛇翻译2.2版本更新日志
1. 加入回车键查询单词  ok
2. 支持有道翻译中英互查  ok
3. 修复谷歌翻译中英互查乱码bug  ok
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
                final_text += span.string
    except AttributeError as e:
        messagebox.showinfo('提示!', '输入有误,无查询结果!\n请重新输入.')
        return None
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
        tk = js2py.eval_js(js)
        model = re.compile(u'[\u4e00-\u9fa5]')

        if model.search(target):
            tl = 'en'
        else:
            tl = 'zh-CN'

        param = {'tk': tk(target), 'q': target, 'tl': tl}
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


class Window(object):
    def __init__(self):
        self.tk = tkinter.Tk()

        ws = self.tk.winfo_screenwidth()
        hs = self.tk.winfo_screenheight()
        width, height = 600, 400
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)
        self.tk.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.tk.maxsize(width, height)
        self.tk.minsize(width, height)

        self.tk.title('肥蛇翻译 2.2')

        self.label = tkinter.Label(master=self.tk, text='请输入查询内容:', font=('SimSun', 13),
                                   width=15, height=1, pady=3)
        self.label.pack()  # place(x=115, y=8, anchor='nw')

        self.entry = tkinter.Entry(master=self.tk, width=50, font=('SimSun', 12))
        self.entry.pack()  # place(x=60, y=40, anchor='nw')
        self.entry.bind('<Return>', func=self.EnterInput)

        self.clean = tkinter.Button(master=self.tk, text='清空', command=self.cleanAll, width=17, font=('SimSun', 11))
        self.clean.place(x=310, y=56, anchor='nw')

        self.query = tkinter.Button(master=self.tk, text='查询(回车)', command=self.doQuery, width=17, font=('SimSun', 11))
        self.query.place(x=130, y=56, anchor='nw')

        self.label_youdao = tkinter.Label(master=self.tk, text='有道翻译:', font=('SimSun', 10),
                                          width=8, height=1)
        self.label_youdao.place(x=10, y=90, anchor='nw')

        self.label_google = tkinter.Label(master=self.tk, text='谷歌翻译:', font=('SimSun', 10),
                                          width=8, height=1)
        self.label_google.place(x=305, y=90, anchor='nw')

        self.resYoudao = scrolledtext.ScrolledText(self.tk, width=33, height=17, wrap=tkinter.WORD,
                                                   state=tkinter.DISABLED, font=('Arial', 11))
        self.resGoogle = scrolledtext.ScrolledText(self.tk, width=33, height=17, wrap=tkinter.WORD,
                                                   state=tkinter.DISABLED, font=('Arial', 11))

        self.resYoudao.place(x=10, y=115)
        self.resGoogle.place(x=305, y=115)

        self.end = tkinter.Label(master=self.tk, text='------------------------------------------------------------- '
                                                      'FAT SNAKE 2.2'
                                                      ' -------------------------------------------------------------',
                                 font=('Arial', 8))
        self.end.pack(side='bottom')

        self.tk.mainloop()

    def EnterInput(self, event):
        if event.keysym == 'Return':
            self.doQuery()

    def cleanAll(self):
        self.entry.delete(0, tkinter.END)
        self.resYoudao.configure(state=tkinter.NORMAL)
        self.resYoudao.delete(1.0, tkinter.END)
        self.resYoudao.configure(state=tkinter.DISABLED)
        self.resGoogle.configure(state=tkinter.NORMAL)
        self.resGoogle.delete(1.0, tkinter.END)
        self.resGoogle.configure(state=tkinter.DISABLED)

    def doQuery(self):
        res_youdao = getResultYoudao(self.entry.get())
        if res_youdao:
            res_google = getResultGoogle(self.entry.get())
            self.printResultYoudao(res_youdao)
            self.printResultGoogle(res_google)
        else:
            self.cleanAll()

    def printResultYoudao(self, res_youdao):
        self.resYoudao.configure(state=tkinter.NORMAL)
        self.resYoudao.delete(1.0, tkinter.END)
        self.resYoudao.insert(tkinter.INSERT, res_youdao)
        self.resYoudao.configure(state=tkinter.DISABLED)

    def printResultGoogle(self, res_google):
        self.resGoogle.configure(state=tkinter.NORMAL)
        self.resGoogle.delete(1.0, tkinter.END)
        self.resGoogle.insert(tkinter.INSERT, res_google)
        self.resGoogle.configure(state=tkinter.DISABLED)


if __name__ == '__main__':
    win = Window()
