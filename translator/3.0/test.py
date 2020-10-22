"""
Get
text
from and put
text
on
the
clipboard.
"""

import wx


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Accessing the clipboard', size=(400, 300))

        # Components
        self.panel = wx.Panel(self)
        self.text = wx.TextCtrl(self.panel, pos=(10, 10), size=(370, 220))
        self.copy = wx.Button(self.panel, wx.ID_ANY, label='Copy', pos=(10, 240))
        self.paste = wx.Button(self.panel, wx.ID_ANY, label='Paste', pos=(100, 240))

        # Event bindings.
        self.Bind(wx.EVT_BUTTON, self.OnCopy, self.copy)
        self.Bind(wx.EVT_BUTTON, self.OnPaste, self.paste)

    def OnCopy(self, event):
        text_obj = wx.TextDataObject()
        text_obj.SetText(self.text.GetValue())
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
            wx.TheClipboard.SetData(text_obj)
            wx.TheClipboard.Close()

    def OnPaste(self, event):
        text_obj = wx.TextDataObject()
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
            if wx.TheClipboard.GetData(text_obj):
                self.text.SetValue(text_obj.GetText())
            wx.TheClipboard.Close()


app = wx.App(False)
frame = MyFrame()
frame.Show(True)
app.MainLoop()
