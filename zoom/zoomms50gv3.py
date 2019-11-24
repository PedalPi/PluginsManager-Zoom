from zoom.observer.host.zoom_ms.zoom_ms_host import ZoomMSHost
from zoom.observer.zoom_host import ZoomHost
from zoom.zoom_equipment import ZoomEquipment


class ZoomMS50gv3(ZoomEquipment):

    def __init__(self):
        super().__init__()
        self._total_pedalboards = 50

    def connect(self):
        self.host = ZoomHost(ZoomMSHost)
        self.register(self.host)
        self.host.connect(self)
