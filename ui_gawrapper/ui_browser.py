__author__ = 'Daniil Leksin'
import wx
import wx.html2


class Browser(wx.Panel):
    def __init__(self, parent, frame=None):
        wx.Panel.__init__(self, parent, -1)

        self.current = 'https://developers.google.com/analytics//'
        self.frame = frame
        if frame:
            self.titleBase = frame.GetTitle()

        sz_main = wx.BoxSizer(wx.VERTICAL)
        sz_buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.web_view = wx.html2.WebView.New(self)
        self.Bind(wx.html2.EVT_WEBVIEW_LOADED, self.on_web_view_loaded, self.web_view)

        self.cb_online_help = wx.CheckBox(self, wx.ID_ANY, u"Use online help!", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cb_online_help.Value = True
        self.cb_online_help.Disable()
        sz_buttons.Add(self.cb_online_help, 0, wx.EXPAND | wx.ALL, 2)

        bt_back = wx.Button(self, -1, "<--", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.on_bt_back, bt_back)
        sz_buttons.Add(bt_back, 0, wx.EXPAND | wx.ALL, 2)
        self.Bind(wx.EVT_UPDATE_UI, self.on_check_valid_back, bt_back)

        btn_forward = wx.Button(self, -1, "-->", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.on_bt_forward, btn_forward)
        sz_buttons.Add(btn_forward, 0, wx.EXPAND | wx.ALL, 2)
        self.Bind(wx.EVT_UPDATE_UI, self.on_check_valid_forward, btn_forward)

        bt_stop = wx.Button(self, -1, "Stop", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.on_bt_stop, bt_stop)
        sz_buttons.Add(bt_stop, 0, wx.EXPAND | wx.ALL, 2)

        bt_refresh = wx.Button(self, -1, "Refresh", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.on_bt_refresh, bt_refresh)
        sz_buttons.Add(bt_refresh, 0, wx.EXPAND | wx.ALL, 2)

        txt = wx.StaticText(self, -1, "URL:")
        sz_buttons.Add(txt, 0, wx.CENTER | wx.ALL, 2)

        self.location = wx.ComboBox(
            self, -1, "", style=wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER)
        self.location.AppendItems(['https://developers.google.com/analytics/'])
        self.Bind(wx.EVT_COMBOBOX, self.on_select_location, self.location)
        self.location.Bind(wx.EVT_TEXT_ENTER, self.on_location_enter)
        sz_buttons.Add(self.location, 1, wx.EXPAND | wx.ALL, 2)

        sz_main.Add(sz_buttons, 0, wx.EXPAND)
        sz_main.Add(self.web_view, 1, wx.EXPAND)
        self.SetSizer(sz_main)

        self.web_view.LoadURL(self.current)

    def on_web_view_loaded(self, event):
        # The full document has loaded
        self.current = event.GetURL()
        self.location.SetValue(self.current)

    # Control bar events
    def on_select_location(self, event):
        url = self.location.GetStringSelection()
        self.web_view.LoadURL(url)

    def on_location_enter(self, event=None):
        url = self.location.GetValue()
        self.location.Append(url)
        self.web_view.LoadURL(url)

    def on_bt_back(self, event):
        self.web_view.GoBack()

    def on_bt_forward(self, event):
        self.web_view.GoForward()

    def on_check_valid_back(self, event):
        event.Enable(self.web_view.CanGoBack())

    def on_check_valid_forward(self, event):
        event.Enable(self.web_view.CanGoForward())

    def on_bt_stop(self, event):
        self.web_view.Stop()

    def on_bt_refresh(self, event):
        self.web_view.Reload()
