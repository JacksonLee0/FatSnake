#!/usr/bin/python
# -*- coding: UTF-8 -*
# -
import tkinter
import urllib
from tkinter import messagebox
from tkinter import scrolledtext

import execjs
import requests
from bs4 import BeautifulSoup


def getResultYoudao(content):
    query = urllib.parse.quote(content)
    url = 'http://www.youdao.com/w/' + query + '/#keyfrom=dict2.top'
    req = requests.get(url=url)
    bf = BeautifulSoup(req.text, features="html.parser")
    body = bf.body
    final_res = []
    try:
        result_contents = body.find('div', class_='results-content')

        if result_contents.find('div', id='phrsListTab', class_='trans-wrapper clearfix') is not None:
            trans_container = body.find('div', class_='trans-container')
            ul = trans_container.find('ul')
            li = ul.find_all('li')
            for item in li:
                final_res.append(item.string)
            final_res.append('(以上来自有道词典)\n')

        if result_contents.find('div', id='webTrans', class_='trans-wrapper trans-tab') is not None:
            sign = False
            wt_container = body.find('div', id='tWebTrans', class_='trans-container tab-content')
            title = wt_container.find_all('div', class_='title')
            for item in title:
                if item.find('span') is not None:
                    span = item.find('span')
                    sign = True
                    final_res.append(span.string.strip())

            if sign is True:
                final_res.append('(以上来自网络释义)\n')

        if result_contents.find('div', id='ydTrans', class_='trans-wrapper') is not None:
            trans_container = body.find('div', class_='trans-container')
            p = trans_container.find_all('p')
            final_res.append(p[1].string)
            final_res.append('(以上来自有道翻译)\n')

        if result_contents.find('div', class_='error-wrapper'):
            error = body.find('div', class_='error-typo')
            p = error.find_all('p', class_='typo-rel')
            final_res.append('猜您要找的是不是: ')
            for i in p:
                span = i.find('span', class_='title')
                final_res.append(span.string)
    except AttributeError as e:
        messagebox.showinfo('提示!', '输入有误,无查询结果!\n请重新输入.')

    final_text = ''
    for item in final_res:
        if item is not None:  # 1.1 版本更新,解决部分单词错误
            final_text += item + '\n'
    return final_text


def getResultGoogle(target):
    allText = ''
    if target == '':
        return allText
    else:
        ctx = execjs.compile(
            '''
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
                '''
        )
        param = {'tk': ctx.call('TL', target), 'q': target}
        result = requests.get("""https://translate.google.co.uk/translate_a/single?client=webapp&sl=auto&tl=zh-CN&hl=en
            &dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&source=bh&ssel=0&tsel=0&kc=1""", params=param)

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


# INTERFACE ---
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

        self.tk.title('肥蛇翻译')

        self.label = tkinter.Label(master=self.tk, text='请输入查询内容:', font=('SimSun', 13),
                                   width=15, height=1, pady=3)
        self.label.pack()  # place(x=115, y=8, anchor='nw')

        self.entry = tkinter.Entry(master=self.tk, width=50, font=('Arial', 12))
        self.entry.pack()  # place(x=60, y=40, anchor='nw')

        self.clean = tkinter.Button(master=self.tk, text='清空', command=self.cleanAll, width=17, font=('SimSun', 11))
        self.clean.place(x=310, y=56, anchor='nw')

        self.query = tkinter.Button(master=self.tk, text='查询', command=self.doQuery, width=17, font=('SimSun', 11))
        self.query.place(x=130, y=56, anchor='nw')

        self.label_youdao = tkinter.Label(master=self.tk, text='有道翻译:', font=('SimSun', 10),
                                          width=8, height=1)
        self.label_youdao.place(x=10, y=90, anchor='nw')

        self.label_google = tkinter.Label(master=self.tk, text='谷歌翻译:', font=('SimSun', 10),
                                          width=8, height=1)
        self.label_google.place(x=305, y=90, anchor='nw')

        self.resYoudao = scrolledtext.ScrolledText(self.tk, width=33, height=17, wrap=tkinter.WORD,
                                                   state=tkinter.DISABLED, font=('SimSun', 11))
        self.resGoogle = scrolledtext.ScrolledText(self.tk, width=33, height=17, wrap=tkinter.WORD,
                                                   state=tkinter.DISABLED, font=('SimSun', 11))

        self.resYoudao.place(x=10, y=115)
        self.resGoogle.place(x=305, y=115)

        self.end = tkinter.Label(master=self.tk, text='------------------------------------------------ FAT SNAKE '
                                                      '------------------------------------------------',
                                 font=('Arial', 8))
        self.end.pack(side='bottom')

        self.tk.mainloop()

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
        res_google = getResultGoogle(self.entry.get())
        self.printResultYoudao(res_youdao)
        self.printResultGoogle(res_google)

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
