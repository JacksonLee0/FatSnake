import wx


# 子类化框架类
class MyFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'My Frame', size=(300, 300))
        panel = wx.Panel(self, -1)
        panel.Bind(wx.EVT_MOTION, self.OnMove)
        wx.StaticText(panel, -1, 'pos:', pos=(30, 62))  # 创建静态文本控件
        self.posCtrl = wx.TextCtrl(panel, -1, '', pos=(60, 60), size=(160, 24), style=wx.TE_CENTER)  # 创建文本框控件

    # 创建鼠标移动事件
    def OnMove(self, event):
        pos = event.GetPosition()
        self.posCtrl.SetValue("%s,%s" % (pos.x, pos.y))


if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyFrame()
    frame.Show(True)
    app.MainLoop()
