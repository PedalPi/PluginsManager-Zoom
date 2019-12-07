from zoom.observer.host.zoom_g1on.zoom_g1on_host import ZoomG1onHost
from zoom.observer.zoom_host import ZoomHost
from zoom.zoom_equipment import ZoomEquipment


class ZoomG1on(ZoomEquipment):

    def __init__(self):
        super().__init__()
        self._total_pedalboards = 100

    def connect(self):
        self.host = ZoomHost(ZoomG1onHost())
        self.register(self.host)
        self.host.connect(self)
