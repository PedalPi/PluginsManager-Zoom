from zoom.observer.host.base.zoom_equipment_host import ZoomEquipmentHostData
from zoom.observer.host.zoom_ms.zoom_ms_message_decoder import ZoomMSMessageDecoder
from zoom.observer.host.zoom_ms.zoom_ms_message_encoder import ZoomMSMessageEncoder
from zoom.zoom_model import ZoomModel, Manufacturer


class ZoomMSHost(ZoomEquipmentHostData):
    """
    Comunicate with Zoom ZFX-IV processor device MS series
    """

    def __init__(self):
        super().__init__()
        self.manufacturer = Manufacturer.Zoom
        self.device_id = 0x00
        self.model = ZoomModel.ZoomMS50g

        self.name = 'ZOOM MS Series MIDI 1'

        self.encoder_class = ZoomMSMessageEncoder
        self.decoder_class = ZoomMSMessageDecoder
