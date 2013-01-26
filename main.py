import c600
import gui
import wx

class C600GUI(wx.App):
  def __init__(self):
    self._device = c600.C600()
    self._app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    self._frame = gui.GUI(None, -1, "")

    def CreateLevelChangeCallback(mixer, chan_type, chan_index):
      def OnLevelChange(event):
        self._device.SetLevel(mixer, chan_type, chan_index,
                              event.GetEventObject().GetValue() / 100.0)
      return OnLevelChange

    for m in xrange(4):
      mixer = getattr(self._frame, 'mixer_{}'.format(m))
      for i in xrange(6):
        channel = getattr(mixer, 'input_{}'.format(i))
        channel.channel_label.SetLabel('in {}'.format(i + 1))
        channel.level_slider.Bind(
          wx.EVT_SCROLL,
          CreateLevelChangeCallback(m, c600.CHAN_INPUT, i))
      for r in xrange(8):
        channel = getattr(mixer, 'return_{}'.format(r))
        channel.channel_label.SetLabel('ret {}'.format(r + 1))
        channel.level_slider.Bind(
          wx.EVT_SCROLL,
          CreateLevelChangeCallback(m, c600.CHAN_RETURN, r))

    self._app.SetTopWindow(self._frame)
    self._frame.Show()

  def MainLoop(self):
    self._app.MainLoop()


if __name__ == "__main__":
  c600gui = C600GUI()
  c600gui.MainLoop()