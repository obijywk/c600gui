#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.4 on Sat Jan 26 15:49:18 2013

import wx

# begin wxGlade: extracode
# end wxGlade


class GUI(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: GUI.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.mixer_tabs = wx.Notebook(self, -1, style=0)
        self.mixer_0_tab = wx.Panel(self.mixer_tabs, -1)
        self.mixer_0 = MixerPanel(self.mixer_0_tab, -1)
        self.mixer_1_tab = wx.Panel(self.mixer_tabs, -1)
        self.mixer_1 = MixerPanel(self.mixer_1_tab, -1)
        self.mixer_2_tab = wx.Panel(self.mixer_tabs, -1)
        self.mixer_2 = MixerPanel(self.mixer_2_tab, -1)
        self.mixer_3_tab = wx.Panel(self.mixer_tabs, -1)
        self.mixer_3 = MixerPanel(self.mixer_3_tab, -1)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: GUI.__set_properties
        self.SetTitle("C600 GUI")
        self.SetSize((800, 600))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: GUI.__do_layout
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        mixer_3_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mixer_2_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mixer_1_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mixer_0_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mixer_0_sizer.Add(self.mixer_0, 1, wx.EXPAND, 0)
        self.mixer_0_tab.SetSizer(mixer_0_sizer)
        mixer_1_sizer.Add(self.mixer_1, 1, wx.EXPAND, 0)
        self.mixer_1_tab.SetSizer(mixer_1_sizer)
        mixer_2_sizer.Add(self.mixer_2, 1, wx.EXPAND, 0)
        self.mixer_2_tab.SetSizer(mixer_2_sizer)
        mixer_3_sizer.Add(self.mixer_3, 1, wx.EXPAND, 0)
        self.mixer_3_tab.SetSizer(mixer_3_sizer)
        self.mixer_tabs.AddPage(self.mixer_0_tab, "Analog 1/2")
        self.mixer_tabs.AddPage(self.mixer_1_tab, "Analog 3/4")
        self.mixer_tabs.AddPage(self.mixer_2_tab, "Analog 5/6")
        self.mixer_tabs.AddPage(self.mixer_3_tab, "S/PDIF L/R")
        frame_sizer.Add(self.mixer_tabs, 1, wx.EXPAND, 0)
        self.SetSizer(frame_sizer)
        self.Layout()
        # end wxGlade

# end of class GUI

class MixerPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MixerPanel.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.input_0 = ChannelPanel(self, -1)
        self.input_1 = ChannelPanel(self, -1)
        self.input_2 = ChannelPanel(self, -1)
        self.input_3 = ChannelPanel(self, -1)
        self.input_4 = ChannelPanel(self, -1)
        self.input_5 = ChannelPanel(self, -1)
        self.return_0 = ChannelPanel(self, -1)
        self.return_1 = ChannelPanel(self, -1)
        self.return_2 = ChannelPanel(self, -1)
        self.return_3 = ChannelPanel(self, -1)
        self.return_4 = ChannelPanel(self, -1)
        self.return_5 = ChannelPanel(self, -1)
        self.return_6 = ChannelPanel(self, -1)
        self.return_7 = ChannelPanel(self, -1)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MixerPanel.__set_properties
        self.SetSize((802, 502))
        self.input_0.SetMinSize((32, 500))
        self.input_1.SetMinSize((32, 500))
        self.input_2.SetMinSize((32, 500))
        self.input_3.SetMinSize((32, 500))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MixerPanel.__do_layout
        channel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        channel_sizer.Add(self.input_0, 1, wx.EXPAND, 0)
        channel_sizer.Add(self.input_1, 1, wx.EXPAND, 0)
        channel_sizer.Add(self.input_2, 1, wx.EXPAND, 0)
        channel_sizer.Add(self.input_3, 1, wx.EXPAND, 0)
        channel_sizer.Add(self.input_4, 1, wx.EXPAND, 0)
        channel_sizer.Add(self.input_5, 1, wx.EXPAND, 0)
        channel_sizer.Add(self.return_0, 1, wx.EXPAND, 0)
        channel_sizer.Add(self.return_1, 1, wx.EXPAND, 0)
        channel_sizer.Add(self.return_2, 1, wx.EXPAND, 0)
        channel_sizer.Add(self.return_3, 1, wx.EXPAND, 0)
        channel_sizer.Add(self.return_4, 1, wx.EXPAND, 0)
        channel_sizer.Add(self.return_5, 1, wx.EXPAND, 0)
        channel_sizer.Add(self.return_6, 1, wx.EXPAND, 0)
        channel_sizer.Add(self.return_7, 1, wx.EXPAND, 0)
        self.SetSizer(channel_sizer)
        # end wxGlade

# end of class MixerPanel

class ChannelPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ChannelPanel.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.level_gauge = wx.Gauge(self, -1, 10, style=wx.GA_VERTICAL | wx.GA_SMOOTH)
        self.level_slider = wx.Slider(self, -1, 0, 0, 100, style=wx.SL_VERTICAL | wx.SL_AUTOTICKS | wx.SL_LABELS | wx.SL_LEFT | wx.SL_SELRANGE | wx.SL_INVERSE)
        self.channel_label = wx.StaticText(self, -1, "1")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ChannelPanel.__set_properties
        self.SetSize((34, 502))
        self.level_gauge.SetMinSize((20, 180))
        self.level_slider.SetMinSize((32, 300))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ChannelPanel.__do_layout
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.level_gauge, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_2.Add(self.level_slider, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_2.Add(self.channel_label, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetSizer(sizer_2)
        # end wxGlade

# end of class ChannelPanel
if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    main_frame = GUI(None, -1, "")
    app.SetTopWindow(main_frame)
    main_frame.Show()
    app.MainLoop()
