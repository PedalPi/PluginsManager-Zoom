import mido

from zoom.observer.host.protocol import MidiProtocol
from zoom.observer.host.zoom_iv_connection import ZoomIVConnection
from zoom.observer.host.zoom_iv_message_decoder import ZoomIVMessageDecoder
from zoom.observer.host.zoom_iv_message_encoder import ZoomIVMessageEncoder


class ZoomIVHost:
    """
    Comunicate with Zoom ZFX-IV processor device
    """

    def __init__(self, context):
        self.manufacturing_id = 0x52
        self.device_id = 0x00
        self.model_number = 0x5A

        self.name = 'ZOOM G Series MIDI 1'

        self.connection = ZoomIVConnection(self.name)
        self.connection.callback = lambda message: self.decode(message)
        self.message_encoder = ZoomIVMessageEncoder(self.manufacturing_id, self.device_id, self.model_number)
        self.message_decoder = ZoomIVMessageDecoder(context)

    def initialize(self):
        device_info = mido.Message('sysex', data=MidiProtocol.device_identify_request())

        self.connection.send(device_info)
        self.connection.send(self.message_encoder.enable_editor())

    def close(self):
        self.connection.send(self.message_encoder.disable_editor())

    def decode(self, message):
        self.message_decoder.decode(message)
