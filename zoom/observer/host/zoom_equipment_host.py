import mido

from zoom.observer.host.protocol import MidiProtocol
from zoom.observer.host.zoom_connection import ZoomConnection


class ZoomEquipmentHostData:
    def __init__(self):
        self.manufacturing_id = None
        self.device_id = None
        self.model_number = None

        self.name = None

        self.connection_class = None
        self.encoder_class = None
        self.decoder_class = None


class ZoomEquipmentHost:

    def __init__(self, context, host_data: ZoomEquipmentHostData):
        self.host_data = host_data

        MessageEncoder = self.host_data.encoder_class
        MessageDecoder = self.host_data.decoder_class

        self.connection = ZoomConnection(self.host_data.name)
        self.connection.callback = lambda message: self.decode(message)

        self.message_encoder = MessageEncoder(
            self.host_data.manufacturing_id,
            self.host_data.device_id,
            self.host_data.model_number
        )
        self.message_decoder = MessageDecoder(context)

    def initialize(self):
        device_info = mido.Message('sysex', data=MidiProtocol.device_identify_request())

        self.connection.send(device_info)
        self.connection.send(self.message_encoder.enable_editor())

    def close(self):
        self.connection.send(self.message_encoder.disable_editor())

    def decode(self, message):
        self.message_decoder.decode(message)

