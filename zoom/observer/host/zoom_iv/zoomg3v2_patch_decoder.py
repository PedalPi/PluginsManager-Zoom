from zoom.model.zoom_pedalboard import ZoomPedalboard
from zoom.observer.host.zoom_patch_decoder import ZoomPatchDecoder
from zoom.zoom_model import ZoomModel


class ZoomG3v2PatchDecoder(ZoomPatchDecoder):

    @property
    def effects_status_bits(self):
        return [
            [(0+4, 1, 0)],
            [(13+4, 1, 0)],
            [(27+4, 1, 0)],
            [(41+4, 1, 0)],
            [(54+4, 1, 0)],
            [(68+4, 1, 0)]
        ]

    @property
    def effects_bits(self):
        # From: decoder/retriever/patch_effects_save_data.py
        # From: decoder/patch_effects_decode.py
        # (position, mask, shift)
        return [
            [(10, 126, -1), (9, 64, 0)],
            [(23, 126, -1), (17, 2, 5)],
            [(37, 126, -1), (33, 8, 3)],
            [(51, 126, -1), (49, 32, 1)],
            [(64, 126, -1), (57, 1, 6)],
            [(78, 126, -1), (73, 4, 4)]
        ]

    @property
    def params_bits(self):
        # From: decoder/retriever/patch_params_save_data.py
        # From: decoder/patch_params_decode.py
        # (position, mask, shift)
        return [
            [[(11, 126, -1), (9, 32, 1), (12, 31, 7)], [(12, 64, -6), (9, 16, -3), (13, 127, 2), (9, 8, 6)], [(14, 120, -3), (9, 4, 2), (15, 63, 5)], [(16, 127, 0), (9, 1, 7)], [(18, 127, 0), (17, 64, 1)], [(19, 127, 0), (17, 32, 2)], [(20, 127, 0), (17, 16, 3)], [(21, 127, 0), (17, 8, 4)]],
            [[(24, 126, -1), (17, 1, 6), (26, 31, 7)], [(26, 64, -6), (25, 64, -5), (27, 127, 2), (25, 32, 4)], [(28, 120, -3), (25, 16, 0), (29, 63, 5)], [(30, 127, 0), (25, 4, 5)], [(31, 127, 0), (25, 2, 6)], [(32, 127, 0), (25, 1, 7)], [(34, 127, 0), (33, 64, 1)], [(35, 127, 0), (33, 32, 2)]],
            [[(38, 126, -1), (33, 4, 4), (39, 31, 7)], [(39, 64, -6), (33, 2, 0), (40, 127, 2), (33, 1, 9)], [(42, 120, -3), (41, 64, -2), (43, 63, 5)], [(44, 127, 0), (41, 16, 3)], [(45, 127, 0), (41, 8, 4)], [(46, 127, 0), (41, 4, 5)], [(47, 127, 0), (41, 2, 6)], [(48, 127, 0), (41, 1, 7)]],
            [[(52, 126, -1), (49, 16, 2), (53, 31, 7)], [(53, 64, -6), (49, 8, -2), (54, 127, 2), (49, 4, 7)], [(55, 120, -3), (49, 2, 3), (56, 63, 5)], [(58, 127, 0), (57, 64, 1)], [(59, 127, 0), (57, 32, 2)], [(60, 127, 0), (57, 16, 3)], [(61, 127, 0), (57, 8, 4)], [(62, 127, 0), (57, 4, 5)]],
            [[(66, 126, -1), (65, 64, 0), (67, 31, 7)], [(67, 64, -6), (65, 32, -4), (68, 127, 2), (65, 16, 5)], [(69, 120, -3), (65, 8, 1), (70, 63, 5)], [(71, 127, 0), (65, 2, 6)], [(72, 127, 0), (65, 1, 7)], [(74, 127, 0), (73, 64, 1)], [(75, 127, 0), (73, 32, 2)], [(76, 127, 0), (73, 16, 3)]],
            [[(79, 126, -1), (73, 2, 5), (80, 31, 7)], [(80, 64, -6), (73, 1, 1), (82, 127, 2), (81, 64, 3)], [(83, 120, -3), (81, 32, -1), (84, 63, 5)], [(85, 127, 0), (81, 8, 4)], [(86, 127, 0), (81, 4, 5)], [(87, 127, 0), (81, 2, 6)], [(88, 127, 0), (81, 1, 7)], [(90, 127, 0), (89, 64, 1)]]
        ]

    def __init__(self):
        super().__init__(ZoomModel.ZoomG3v2)

    def decode(self, data, pedalboard: ZoomPedalboard) -> ZoomPedalboard:
        equipment_info = self.equipment_info(data)

        pedalboard.name = bytes(data[0x65:0x69] + data[0x6A:0x70]).decode()

        for id_effect in range(6):
            effect = self.decode_effect(data, id_effect)
            self.put_effect(pedalboard, effect, id_effect)

        pedalboard.level = data[0x5c]

        # TODO: Display info
        # ...
        # TODO: CTRL SW/PDL
        # ...
        # TODO: PDL DST
        # ...

        return pedalboard
