from zoom.observer.host.base.zoom_equipment_host import ZoomEquipmentHostData
from zoom.observer.host.zoom_iv.zoom_iv_message_decoder import ZoomIVMessageDecoder
from zoom.observer.host.zoom_iv.zoom_iv_message_encoder import ZoomIVMessageEncoder
from zoom.zoom_model import ZoomModel, Manufacturer


class ZoomG1onHost(ZoomEquipmentHostData):
    """
    Comunicate with Zoom ZFX-IV processor device
    """

    def __init__(self):
        super().__init__()
        self.manufacturing_id = Manufacturer.Zoom
        self.device_id = 0x00
        self.model_number = ZoomModel.ZoomG1on

        self.name = 'ZOOM 1 Series MIDI 1'

        # FIXME
        self.encoder_class = ZoomIVMessageEncoder
        self.decoder_class = ZoomIVMessageDecoder
