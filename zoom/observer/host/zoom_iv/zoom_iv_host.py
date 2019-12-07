from zoom.observer.host.zoom_equipment_host import ZoomEquipmentHostData
from zoom.observer.host.zoom_iv.zoom_iv_message_decoder import ZoomIVMessageDecoder
from zoom.observer.host.zoom_iv.zoom_iv_message_encoder import ZoomIVMessageEncoder
from zoom.zoom_model import ZoomModel, Manufacturer


class ZoomIVHost(ZoomEquipmentHostData):
    """
    Comunicate with Zoom ZFX-IV processor device
    """

    def __init__(self):
        super().__init__()
        self.manufacturing_id = Manufacturer.Zoom
        self.device_id = 0x00
        self.model_number = ZoomModel.ZoomG3v2

        self.name = 'ZOOM G Series MIDI 1'

        self.encoder_class = ZoomIVMessageEncoder
        self.decoder_class = ZoomIVMessageDecoder
