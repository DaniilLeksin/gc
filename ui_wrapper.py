__author__ = 'Daniil Leksin'
# -*- coding: utf-8 -*-

###########################################################################
##
##
##
##
###########################################################################

import wx
import wx.html
from ui_browser import Browser
from ui_properties import Properties
from c_wrapper import *

###########################################################################
## Class main
###########################################################################


class Main(wx.Frame):
    
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"GA: wrapper", pos=wx.DefaultPosition,
                          size=wx.Size(964, 750), style=wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        sz_main = wx.BoxSizer(wx.VERTICAL)

        sz_top = wx.BoxSizer(wx.HORIZONTAL)

        sz_properties = wx.BoxSizer(wx.HORIZONTAL)

        self.nb_properties = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.p_properties = Properties(self.nb_properties)
        self.nb_properties.AddPage(self.p_properties, u"Properties", True)
        self.p_response = wx.Panel(self.nb_properties, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.nb_properties.AddPage(self.p_response, u"Response", False)

        sz_properties.Add(self.nb_properties, 1, wx.ALL | wx.EXPAND, 5)

        self.hw_info = Browser(self)
        sz_properties.Add(self.hw_info, 1, wx.ALL | wx.EXPAND, 5)

        sz_top.Add(sz_properties, 1, wx.EXPAND, 5)

        sz_main.Add(sz_top, 1, wx.EXPAND, 5)

        sz_bottom = wx.BoxSizer(wx.VERTICAL)

        sz_buttons = wx.BoxSizer(wx.HORIZONTAL)

        self.bt_getData = wx.Button(self, wx.ID_ANY, u"Make report", wx.DefaultPosition, wx.DefaultSize, 0)
        sz_buttons.Add(self.bt_getData, 1, wx.ALL, 5)

        self.bt_clearSelection = wx.Button(self, wx.ID_ANY, u"Clear selections", wx.DefaultPosition, wx.DefaultSize, 0)
        sz_buttons.Add(self.bt_clearSelection, 1, wx.ALL, 5)

        self.bt_save2json = wx.Button(self, wx.ID_ANY, u"Save to json format", wx.DefaultPosition, wx.DefaultSize, 0)
        sz_buttons.Add(self.bt_save2json, 1, wx.ALL, 5)

        self.bt_save2wrapper = wx.Button(self, wx.ID_ANY, u"Save to wrapper format", wx.DefaultPosition, wx.DefaultSize, 0)
        sz_buttons.Add(self.bt_save2wrapper, 1, wx.ALL, 5)

        self.bt_exit = wx.Button(self, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bt_exit.SetToolTipString(u"Go out from my wrapper")

        sz_buttons.Add(self.bt_exit, 0, wx.ALL, 5)

        sz_bottom.Add(sz_buttons, 0, wx.EXPAND, 5)

        sz_logs = wx.BoxSizer(wx.HORIZONTAL)

        self.tc_logs = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE)
        self.tc_logs.SetMinSize(wx.Size(-1, 150))

        sz_logs.Add(self.tc_logs, 1, wx.ALL, 5)

        sz_bottom.Add(sz_logs, 0, wx.EXPAND, 5)

        sz_main.Add(sz_bottom, 0, wx.EXPAND, 5)

        self.SetSizer(sz_main)
        self.Layout()
        self.sb_status = self.CreateStatusBar(3, wx.ST_SIZEGRIP, wx.ID_ANY)
        
        self.Centre(wx.BOTH)
        
        # Connect Events
        self.bt_getData.Bind(wx.EVT_BUTTON, self.on_bt_get_data)
        self.bt_clearSelection.Bind(wx.EVT_BUTTON, self.on_bt_clear_selection)
        self.bt_save2json.Bind(wx.EVT_BUTTON, self.on_bt_save2json)
        self.bt_save2wrapper.Bind(wx.EVT_BUTTON, self.on_bt_save2wrapper)
        self.bt_exit.Bind(wx.EVT_BUTTON, self.on_bt_exit)
    
    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def on_bt_get_data(self, event):
        # Check the correctness of info
        print self.p_properties.dict_api_properties
        #check_the_data(self.hw_info)

    def on_bt_clear_selection(self, event):
        event.Skip()
    
    def on_bt_save2json(self, event):
        event.Skip()
    
    def on_bt_save2wrapper(self, event):
        event.Skip()
    
    def on_bt_exit(self, event):
        event.Skip()

    def set_html_page(self, html_path):
        try:
            if self.hw_info.cb_online_help.IsChecked():
                self.hw_info.location = html_path[1]
                self.hw_info.on_location_enter()
            else:
                self.hw_info.web_view.SetPage(open(html_path[0], 'rb').read())
        except Exception as error:
            print str(error)  # TODO: put in log
