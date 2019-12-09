from zoom.observer.host.base.zoom_equipment_host import ZoomEquipmentHostData
from zoom.observer.host.zoom_g1on.zoom_g1on_message_decoder import ZoomG1onMessageDecoder
from zoom.observer.host.zoom_g1on.zoom_g1on_message_encoder import ZoomG1onMessageEncoder
from zoom.observer.host.zoom_iv.zoom_iv_message_decoder import ZoomIVMessageDecoder
from zoom.observer.host.zoom_iv.zoom_iv_message_encoder import ZoomIVMessageEncoder
from zoom.zoom_model import ZoomModel, Manufacturer


class ZoomG1onHost(ZoomEquipmentHostData):
    """
    Comunicate with Zoom ZFX-IV processor device
    """

    def __init__(self):
        super().__init__()
        self.manufacturer = Manufacturer.Zoom
        self.device_id = 0x00
        self.model = ZoomModel.ZoomG1on

        self.name = 'ZOOM 1 Series MIDI 1'

        self.encoder_class = ZoomG1onMessageEncoder
        self.decoder_class = ZoomG1onMessageDecoder
