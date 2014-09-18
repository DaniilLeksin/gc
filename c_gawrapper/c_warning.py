__author__ = 'Daniil Leksin'
# -*- coding: utf-8 -*-

import wx


def show_warning(message, title='Error'):
    """
    Show dialog box
    :param message: Box message
    :param title: Box title
    :return: None
    """
    dlg = wx.MessageDialog(None, message, title, wx.OK | wx.ICON_WARNING)
    dlg.ShowModal()
    dlg.Destroy()