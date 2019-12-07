from enum import Enum


class Manufacturer(Enum):
    Zoom = 0x52


class ZoomModel(Enum):
    ZoomG3v2 = 0x5A

    ZoomMS50g = 0x58
    ZoomMS60b = 0x5F
    ZoomMS7cdr = 0x61

    ZoomG1on = 0x71


class ZoomEquipmentNotImplemented(Exception):
    pass
