import re
import wx
import datetime

bg_size = [415, 900]


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, pos=(1000, 200), size=bg_size, style=wx.FRAME_SHAPED)

        # Text Buffer
        self.text_buffer = []
        self.history_list = []
        self.head_list = []

        # Bg Setting
        bg = wx.Image("bg.png")
        bg.ConvertAlphaToMask()
        self.bitmap = wx.Bitmap(bg)
        r = wx.Region(self.bitmap)
        self.SetShape(r)
        self.mousePos = wx.Point(0, 0)

        # icon Setting
        self.people_img= wx.Image("people.png").ConvertToBitmap()
        self.ai_img = wx.Image("ai.png").ConvertToBitmap()

        # Timer Setting
        self.timer = wx.Timer(self, 0)
        self.Bind(wx.EVT_TIMER, self.update)
        self.timer.Start(1000)  # 1 second interval

        # Name Setting
        font_name = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Microsoft YaHei')
        self.gf_name = wx.StaticText(self, label="宇宙无敌小仙女", pos=(0, 50), size=(415, 20), style=wx.ALIGN_CENTER)
        self.gf_name.SetBackgroundColour((235, 235, 235))
        self.gf_name.SetFont(font_name)

        # Time Setting
        font_time = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Microsoft YaHei')
        self.now_time = wx.StaticText(self, label=datetime.datetime.now().strftime("%H:%M"), pos=(5, 15))
        self.now_time.SetBackgroundColour((235, 235, 235))
        self.now_time.SetFont(font_time)

        # Text Box Setting
        font_text = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Microsoft YaHei')
        self.text_box = wx.TextCtrl(self, pos=(50, 818), size=(280, 40))
        self.text_box.SetFont(font_text)
        self.text_box.SetMaxLength(15)

        # Event Bind
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClickDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftClickUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightClickUp)
        self.Bind(wx.EVT_TEXT_ENTER, self.SubmitText)

    def onPaint(self, event):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bitmap, 0, 0)

    def OnLeftClickDown(self, event):
        self.CaptureMouse()
        pos = event.GetPosition()
        self.mousePos = wx.Point(pos.x, pos.y)

    def OnLeftClickUp(self, event):
        self.ReleaseMouse()

    def OnMouseMotion(self, event):
        if event.Dragging() and event.LeftIsDown():
            pos = self.ClientToScreen(event.GetPosition())
            self.Move((pos.x - self.mousePos.x, pos.y - self.mousePos.y))

    def OnRightClickUp(self, event):
        self.PopupMenu(MyPopupMenu(self), event.GetPosition())

    def update(self, event):
        self.now_time.SetLabel(datetime.datetime.now().strftime("%H:%M"))

    def SubmitText(self, event):
        print(self.text_box.GetValue().strip())
        msg = self.text_box.GetValue().strip()
        if len(self.text_buffer) == 14:
            self.text_buffer = self.text_buffer[1:]
            self.text_buffer.append('p' + msg)
            self.destroy_history()
        else:
            self.text_buffer.append('p' + msg)
        self.text_box.Clear()
        # generate chat history
        self.generate_text_history()
        # AI response
        self.AI_response(msg)
        # generate chat history
        self.generate_text_history()

    def generate_text_history(self):
        font = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Microsoft YaHei')
        if len(self.text_buffer) < 14:
            message = self.text_buffer[-1]
            if message[0] == 'p':
                length = len(message)
                message = " " + message[1:] + " "
                message_context = wx.StaticText(self, label=message, pos=(bg_size[0] - 18 * length - 50, 110 + 50 * (len(self.text_buffer)-1)),
                                                size=(18 * length, 30))
                message_context.SetBackgroundColour((169, 233, 122))
                message_context.SetFont(font)
                self.history_list.append(message_context)
                button = wx.BitmapButton(self, -1, self.people_img, pos=(bg_size[0] - 40, 110 + 50 * (len(self.text_buffer)-1)), size=(30, 30))
                button.SetDefault()
                self.head_list.append(button)
            else:
                length = len(message)
                message = " " + message[1:] + " "
                message_context = wx.StaticText(self, label=message, pos=(50, 110 + 50 * (len(self.text_buffer) - 1)), size=(18 * length, 30))
                message_context.SetBackgroundColour((240, 240, 240))
                message_context.SetFont(font)
                self.history_list.append(message_context)
                button = wx.BitmapButton(self, -1, self.ai_img, pos=(10, 110 + 50 * (len(self.text_buffer) - 1)), size=(30, 30))
                button.SetDefault()
                self.head_list.append(button)
        else:
            for i in range(len(self.text_buffer)):
                message = self.text_buffer[i]
                if message[0] == 'p':
                    length = len(message)
                    message = " " + message[1:] + " "
                    message_context = wx.StaticText(self, label=message, pos=(bg_size[0] - 18*length - 50, 110 + 50 * i), size=(18*length, 30))
                    message_context.SetBackgroundColour((169, 233, 122))
                    message_context.SetFont(font)
                    self.history_list.append(message_context)
                    button = wx.BitmapButton(self, -1, self.people_img, pos=(bg_size[0] - 40, 110 + 50 * i), size=(30, 30))
                    button.SetDefault()
                    self.head_list.append(button)
                else:
                    length = len(message)
                    message = " " + message[1:] + " "
                    message_context = wx.StaticText(self, label=message, pos=(50, 110 + 50 * i), size=(18 * length, 30))
                    message_context.SetBackgroundColour((240, 240, 240))
                    message_context.SetFont(font)
                    self.history_list.append(message_context)
                    button = wx.BitmapButton(self, -1, self.ai_img, pos=(10, 110 + 50 * i),size=(30, 30))
                    button.SetDefault()
                    self.head_list.append(button)

    def destroy_history(self):
        for i in range(len(self.history_list)):
                self.history_list[i].Destroy()
                self.head_list[i].Destroy()
        self.history_list = []
        self.head_list = []

    def AI_response(self, msg):
        response = "嗯"
        print(msg)
        if re.match(".*在不.*", msg, re.I) or re.match(".*在吗.*", msg, re.I):
            response = "嗯嗯"
        elif re.match(".*在干嘛.*", msg, re.I) or re.match(".*在做啥.*", msg, re.I):
            response = "在想你呀"
        elif re.match(".*情人节.*", msg, re.I):
            response = "情人节快乐~"
        elif re.match(".*老婆.*", msg, re.I):
            response = "嘻嘻嘻"
        elif re.match(".*真的假的.*", msg, re.I):
            response = "你觉得咧"
        elif re.match(".*哈哈.*", msg, re.I):
            response = "笑的好傻"
        elif re.match(".*我.*睡.*", msg, re.I):
            response = "晚安呢？？？？？"
        elif re.match(".*快睡.*", msg, re.I):
            response = "我不"
        elif re.match(".*晚安.*", msg, re.I):
            response = "嘻嘻嘻，晚安晚安~"
        elif re.match("SysCMD()", msg, re.I):
            response = "祝所有程序员小哥哥们早日脱单，幸福快乐~"
        else:
            response = "啊？"

        if len(self.text_buffer) == 14:
            self.text_buffer = self.text_buffer[1:]
            self.text_buffer.append('a' + response)
            try:
                self.destroy_history()
            except:
                pass
        else:
            self.text_buffer.append('a' + response)


class MyPopupMenu(wx.Menu):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        cmi = wx.MenuItem(self, wx.NewId(), 'Close')
        self.AppendItem(cmi)
        self.Bind(wx.EVT_MENU, self.OnClose, cmi)

    def OnClose(self, e):
        self.parent.Close()


class Example(wx.Frame):
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

        self.SetSize((250, 200))
        self.Centre()
        self.Show(True)

    def OnRightDown(self, e):
        self.PopupMenu(MyPopupMenu(self), e.GetPosition())


def main():
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
