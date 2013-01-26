import math
import usb.core
import usb.util

REQ_TYPE_OUT = usb.util.build_request_type(usb.util.CTRL_OUT,
                                           usb.util.CTRL_TYPE_CLASS,
                                           usb.util.CTRL_RECIPIENT_DEVICE)
REQ_TYPE_IN = usb.util.build_request_type(usb.util.CTRL_IN,
                                          usb.util.CTRL_TYPE_CLASS,
                                          usb.util.CTRL_RECIPIENT_INTERFACE)

CHAN_INPUT, CHAN_RETURN = range(2)

class C600(object):
  def __init__(self):
    self._dev = usb.core.find(idVendor=0x0763, idProduct=0x2031)
    if self._dev is None:
      raise ValueError('C600 device not found')

    if not self._dev.get_active_configuration():
      self._dev.set_configuration()

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
    if level == 0.0:
      log_level = 0.0
    else:
      log_level = math.log(level * 1000) / 6.908
    scaled_level = int(0x7FFF * log_level) + 0x8000
    level_bytes = [chr(scaled_level & 0xFF), chr(scaled_level >> 8)]

    result = self._dev.ctrl_transfer(
      REQ_TYPE_OUT, 0x1, value, 0x4001, level_bytes)
    if result != 2:
      raise ValueError('ctrl_transfer failed with result {}'.format(result))

    value += 1
    result = self._dev.ctrl_transfer(
      REQ_TYPE_OUT, 0x1, value, 0x4001, level_bytes)
    if result != 2:
      raise ValueError('ctrl_transfer failed with result {}'.format(result))
