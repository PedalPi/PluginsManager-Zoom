from enum import Enum

from zoom.observer.host.zoom_iv.zoom_iv_host import ZoomIVHost
from zoom.observer.zoom_host import ZoomHost
from zoom.zoom_equipment import ZoomEquipment


class ZoomMS50gv3(ZoomEquipment):

    def connect(self):
        self.host = ZoomHost(ZoomMSHost)
        self.register(self.host)
        self.host.connect(self)
