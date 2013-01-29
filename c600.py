import math
import threading
import usb.core
import usb.util

REQ_TYPE_OUT = usb.util.build_request_type(usb.util.CTRL_OUT,
                                           usb.util.CTRL_TYPE_CLASS,
                                           usb.util.CTRL_RECIPIENT_DEVICE)
REQ_TYPE_IN = usb.util.build_request_type(usb.util.CTRL_IN,
                                          usb.util.CTRL_TYPE_CLASS,
                                          usb.util.CTRL_RECIPIENT_INTERFACE)

CHAN_INPUT, CHAN_RETURN = range(2)

[EFFECT_ROOM_1, EFFECT_ROOM_2, EFFECT_ROOM_3,
 EFFECT_HALL_1, EFFECT_HALL_2,
 EFFECT_PLATE, EFFECT_DELAY, EFFECT_ECHO] = range(8)

def LogLevel(level):
  r"""Convert a human-friendly level to a log adjusted level.

  Args:
    level: float; the human-friendly level (0.0 to 1.0)

  Returns:
    float; the log adjusted level (0.0 to 1.0)
  """
  if level == 0.0:
    return 0.0
  log_level = math.log(level * 1000) / 6.908
  if log_level < 0.0:
    return 0.0
  return log_level

def LevelToByte(level):
  r"""Convert a float level to a list of 1 byte to send.

  Args:
    level: float; the level to send (0.0 to 1.0)

  Returns:
    list of str; the sequence of bytes to send
  """
  return [chr(int(level * 0xFF))]

def LevelToShort(level):
  r"""Convert a float level to a list of 2 bytes to send.

  Args:
    level: float; the level to send (0.0 to 1.0)

  Returns:
    list of str; the sequence of bytes to send
  """
  scaled_level = int(0xFFFE * level + 0x1)
  return [chr(scaled_level & 0xFF), chr(scaled_level >> 8)]

class C600(object):
  def __init__(self, meter_callback=None):
    self._dev = usb.core.find(idVendor=0x0763, idProduct=0x2031)
    if self._dev is None:
      raise ValueError('C600 device not found')

    if not self._dev.get_active_configuration():
      self._dev.set_configuration()

    if meter_callback:
      self._meter_callback = meter_callback
      self._meter_timer = threading.Timer(0.05, self.ReadMeters)
      self._meter_timer.start()

  def SetLevel(self, mixer, chan_type, chan_index, level):
    r"""Sets a mixer level.

    Args:
      mixer: int; the output mixer to adjust (0 to 3)
      chan_type: CHAN_INPUT or CHAN_RETURN; the channel type to adjust
      chan_index: int; the channel to adjust
          (0 to 5 for CHAN_INPUT, 0 to 7 for CHAN_RETURN)
      level: float; the volume level to set (0.0 to 1.0)

    Raises:
      ValueError: An out-of-range value was passed in
    """
    if mixer < 0 or mixer > 3:
      raise ValueError('Invalid mixer {}'.format(mixer))
    if chan_type < 0 or chan_type > 1:
      raise ValueError('Invalid channel type {}'.format(chan_type))
    if (chan_index < 0 or
        (chan_type == CHAN_INPUT and chan_index > 5) or
        (chan_type == CHAN_RETURN and chan_index > 7)):
      raise ValueError('Invalid channel index {}'.format(chan_index))
    if level < 0.0 or level > 1.0:
      raise ValueError('Invalid level {}'.format(level))

    value = 0x100
    if chan_type == CHAN_INPUT:
      value += 0x40
    value += chan_index << 3
    value += mixer << 1

    # TODO: implement stereo pan
    log_level = LogLevel(level) * 0.5 + 0.5
    level_bytes = LevelToShort(log_level)

    result = self._dev.ctrl_transfer(
      REQ_TYPE_OUT, 0x1, value, 0x4001, level_bytes)
    if result != 2:
      raise ValueError('ctrl_transfer failed with result {}'.format(result))

    value += 1
    result = self._dev.ctrl_transfer(
      REQ_TYPE_OUT, 0x1, value, 0x4001, level_bytes)
    if result != 2:
      raise ValueError('ctrl_transfer failed with result {}'.format(result))

  def SetFXSendLevel(self, chan_type, chan_index, level):
    r"""Sets a FX send level.

    Args:
      chan_type: CHAN_INPUT or CHAN_RETURN; the channel type to adjust
      chan_index: int; the channel to adjust
          (0 to 5 for CHAN_INPUT, 0 to 7 for CHAN_RETURN)
      level: float; the FX send level to set (0.0 to 1.0)

    Raises:
      ValueError: An out-of-range value was passed in
    """
    if chan_type < 0 or chan_type > 1:
      raise ValueError('Invalid channel type {}'.format(chan_type))
    if (chan_index < 0 or
        (chan_type == CHAN_INPUT and chan_index > 5) or
        (chan_type == CHAN_RETURN and chan_index > 7)):
      raise ValueError('Invalid channel index {}'.format(chan_index))
    if level < 0.0 or level > 1.0:
      raise ValueError('Invalid level {}'.format(level))

    value = 0x100
    if chan_type == CHAN_INPUT:
      value += 0x08
    value += chan_index

    log_level = LogLevel(level) * 0.5 + 0.5
    level_bytes = LevelToShort(log_level)

    result = self._dev.ctrl_transfer(
      REQ_TYPE_OUT, 0x1, value, 0x4201, level_bytes)
    if result != 2:
      raise ValueError('ctrl_transfer failed with result {}'.format(result))

  def SetFXEffect(self, effect):
    r"""Set the FX effect.

    Args:
      effect: int; the effect to use (0 to 7)

    Raises:
      ValueError: An out-of-range value was passed in
    """
    if effect < 0 or effect > 7:
      raise ValueError('Invalid effect {}'.format(effect))

    result = self._dev.ctrl_transfer(
      REQ_TYPE_OUT, 0x1, 0x200, 0x4301, [chr(effect)])
    if result != 1:
      raise ValueError('ctrl_transfer failed with result {}'.format(result))

  def SetFXDuration(self, duration):
    r"""Set the FX duration.

    Args:
      duration: float; the duration of the effect (0.0 to 1.0)

    Raises:
      ValueError: An out-of-range value was passed in
    """
    if duration < 0.0 or duration > 1.0:
      raise ValueError('Invalid duration {}'.format(duration))

    level_bytes = LevelToShort(duration)
    result = self._dev.ctrl_transfer(
      REQ_TYPE_OUT, 0x1, 0x400, 0x4301, level_bytes)
    if result != 2:
      raise ValueError('ctrl_transfer failed with result {}'.format(result))

  def SetFXFeedback(self, feedback):
    r"""Set the FX feedback.

    Args:
      feedback: float; the feedback of the effect (0.0 to 1.0)

    Raises:
      ValueError: An out-of-range value was passed in
    """
    if feedback < 0.0 or feedback > 1.0:
      raise ValueError('Invalid feedback {}'.format(feedback))

    level_bytes = LevelToByte(feedback)
    result = self._dev.ctrl_transfer(
      REQ_TYPE_OUT, 0x1, 0x500, 0x4301, level_bytes)
    if result != 1:
      raise ValueError('ctrl_transfer failed with result {}'.format(result))

  def SetFXVolume(self, volume):
    r"""Set the FX volume.

    Args:
      volume: float; the volume of the effect (0.0 to 1.0)

    Raises:
      ValueError: An out-of-range value was passed in
    """
    if volume < 0.0 or volume > 1.0:
      raise ValueError('Invalid volume {}'.format(volume))

    level_bytes = LevelToByte(volume)
    result = self._dev.ctrl_transfer(
      REQ_TYPE_OUT, 0x1, 0x300, 0x4301, level_bytes)
    if result != 1:
      raise ValueError('ctrl_transfer failed with result {}'.format(result))

  def SetFXReturn(self, mixer, level):
    r"""Sets an FX return level.

    Args:
      mixer: int; the output mixer to adjust (0 to 3)
      level: float; the volume level to set (0.0 to 1.0)

    Raises:
      ValueError: An out-of-range value was passed in
    """
    if mixer < 0 or mixer > 3:
      raise ValueError('Invalid mixer {}'.format(mixer))
    if level < 0.0 or level > 1.0:
      raise ValueError('Invalid level {}'.format(level))

    value = 0x170
    value += mixer << 1

    # TODO: implement stereo pan
    log_level = LogLevel(level) * 0.5 + 0.5
    level_bytes = LevelToShort(log_level)

    result = self._dev.ctrl_transfer(
      REQ_TYPE_OUT, 0x1, value, 0x4001, level_bytes)
    if result != 2:
      raise ValueError('ctrl_transfer failed with result {}'.format(result))

    value += 0x9
    result = self._dev.ctrl_transfer(
      REQ_TYPE_OUT, 0x1, value, 0x4001, level_bytes)
    if result != 2:
      raise ValueError('ctrl_transfer failed with result {}'.format(result))

  def ReadMeters(self):
    data = self._dev.ctrl_transfer(REQ_TYPE_IN, 0x3, 0x10, 0x2001, 0x32)
    def GetLevel(p):
      level = float((data[p + 1] << 8) + data[p]) / 0xFFFF
      if level == 0.0:
        log_level = 0.0
      else:
        log_level = math.log(level * 1000) / 6.908
        if log_level < 0.0:
          log_level = 0.0
      return log_level
    meter_levels = {}
    for i, p in enumerate(range(0, 12, 2)):
      meter_levels[(CHAN_INPUT, i)] = GetLevel(p)
    for i, p in enumerate(range(12, 28, 2)):
      meter_levels[(CHAN_RETURN, i)] = GetLevel(p)
    self._meter_callback(meter_levels)

    self._meter_timer = threading.Timer(0.1, self.ReadMeters)
    self._meter_timer.start()
