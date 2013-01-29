import c600
import gui
import wx

class C600GUI(wx.App):
  def __init__(self):
    self._app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    self._frame = gui.GUI(None, -1, "")

    self._device = c600.C600(meter_callback=self.MeterCallback)

    def CreateLevelChangeCallback(mixer, chan_type, chan_index):
      def OnLevelChange(event):
        self._device.SetLevel(mixer, chan_type, chan_index,
                              event.GetEventObject().GetValue() / 100.0)
      return OnLevelChange

    def CreateFXReturnChangeCallback(mixer):
      def OnFXReturnChange(event):
        self._device.SetFXReturn(mixer,
                                 event.GetEventObject().GetValue() / 100.0)
      return OnFXReturnChange

    for m in xrange(4):
      mixer = getattr(self._frame, 'mixer_{}'.format(m))
      mixer.fx_return_slider.Bind(wx.EVT_SCROLL,
                                  CreateFXReturnChangeCallback(m))
      for i in xrange(6):
        channel = getattr(mixer, 'input_{}'.format(i))
        channel.channel_label.SetLabel('in {}'.format(i + 1))
        channel.level_gauge.SetRange(100)
        channel.level_slider.Bind(
          wx.EVT_SCROLL,
          CreateLevelChangeCallback(m, c600.CHAN_INPUT, i))
      for r in xrange(8):
        channel = getattr(mixer, 'return_{}'.format(r))
        channel.channel_label.SetLabel('ret {}'.format(r + 1))
        channel.level_gauge.SetRange(100)
        channel.level_slider.Bind(
          wx.EVT_SCROLL,
          CreateLevelChangeCallback(m, c600.CHAN_RETURN, r))

    def CreateFXSendChangeCallback(chan_type, chan_index):
      def OnFXSendChange(event):
        self._device.SetFXSendLevel(chan_type, chan_index,
                                    event.GetEventObject().GetValue() / 100.0)
      return OnFXSendChange

    for i in xrange(6):
      slider = getattr(self._frame, 'fx_send_input_{}_slider'.format(i))
      slider.Bind(wx.EVT_SCROLL,
                  CreateFXSendChangeCallback(c600.CHAN_INPUT, i))
    for r in xrange(8):
      slider = getattr(self._frame, 'fx_send_return_{}_slider'.format(i))
      slider.Bind(wx.EVT_SCROLL,
                  CreateFXSendChangeCallback(c600.CHAN_RETURN, i))

    def OnFXEffectChange(event):
      self._device.SetFXEffect(event.GetEventObject().GetSelection())
    self._frame.fx_choice.Bind(wx.EVT_CHOICE, OnFXEffectChange)

    def OnFXDurationChange(event):
      self._device.SetFXDuration(event.GetEventObject().GetValue() / 100.0)
    self._frame.fx_duration_slider.Bind(wx.EVT_SCROLL, OnFXDurationChange)

    def OnFXFeedbackChange(event):
      self._device.SetFXFeedback(event.GetEventObject().GetValue() / 100.0)
    self._frame.fx_feedback_slider.Bind(wx.EVT_SCROLL, OnFXFeedbackChange)

    def OnFXVolumeChange(event):
      self._device.SetFXVolume(event.GetEventObject().GetValue() / 100.0)
    self._frame.fx_volume_slider.Bind(wx.EVT_SCROLL, OnFXVolumeChange)

    self._app.SetTopWindow(self._frame)
    self._frame.Show()

  def MeterCallback(self, meter_levels):
    current_page = self._frame.mixer_tabs.GetCurrentPage()
    for m in xrange(4):
      if getattr(self._frame, 'mixer_{}_tab'.format(m)) != current_page:
        continue
      mixer = getattr(self._frame, 'mixer_{}'.format(m))
      for channel, level in meter_levels.iteritems():
        if channel[0] == c600.CHAN_INPUT:
          panel = getattr(mixer, 'input_{}'.format(channel[1]))
          panel.level_gauge.SetValue(int(level * 100))
        elif channel[0] == c600.CHAN_RETURN:
          panel = getattr(mixer, 'return_{}'.format(channel[1]))
          panel.level_gauge.SetValue(int(level * 100))

  def MainLoop(self):
    self._app.MainLoop()


if __name__ == "__main__":
  c600gui = C600GUI()
  c600gui.MainLoop()
