__author__ = 'Daniil Leksin'
# -*- coding: utf-8 -*-

import wx

from ui_gawrapper.ui_wrapper import Main


if __name__ == '__main__':
    app = wx.App()
    win = Main(parent=None)
    win.Show()
    app.MainLoop()