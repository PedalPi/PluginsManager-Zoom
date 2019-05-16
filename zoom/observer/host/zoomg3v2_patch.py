from decoder.lib.decoder_util import shift_bits
from zoom.model.zoom.zoom_effect import ZoomEffect


class ZoomG3v2Patch:
    # Append the index by 4 and mask with 0b00000001
    effects_status = [0, 13, 27, 41, 54, 68]

    effects = [0]

    # From: decoder/patch_params_save_data.py
    # From: decoder/patch_params_decoder.py
    # (position, mask, shift)
    params_bits = [
        [[(11, 126, -1), (9, 32, 1), (12, 15, 7)], [(9, 16, -4), (13, 127, 1)], [(14, 120, -3), (9, 4, 2), (15, 31, 5)],
         [(16, 127, 0)], [(18, 127, 0)], [(19, 127, 0)], [(20, 127, 0)], [(21, 127, 0)]],
        [[(24, 126, -1), (17, 1, 6), (26, 15, 7)], [(25, 64, -6), (27, 127, 1)],
         [(28, 120, -3), (25, 16, 0), (29, 31, 5)], [(30, 127, 0)], [(31, 127, 0)], [(32, 127, 0)], [(34, 127, 0)],
         [(35, 1, 0), (35, 124, -1)]], [[(38, 126, -1), (33, 4, 4), (39, 15, 7)], [(33, 2, -1), (40, 127, 1)],
                                        [(42, 120, -3), (41, 64, -2), (43, 31, 5)], [(44, 127, 0)], [(45, 127, 0)],
                                        [(46, 127, 0)], [(47, 127, 0)], [(48, 127, 0)]],
        [[(52, 126, -1), (49, 16, 2), (53, 15, 7)], [(54, 4, -2), (54, 7, 1), (54, 112, 0)],
         [(55, 120, -3), (49, 2, 3), (56, 31, 5)], [(58, 127, 0)], [(59, 127, 0)], [(60, 127, 0)], [(61, 127, 0)],
         [(62, 127, 0)]], [[(66, 126, -1), (65, 64, 0), (67, 15, 7)], [(65, 32, -5), (68, 127, 1)],
                           [(69, 120, -3), (65, 8, 1), (70, 31, 5)], [(71, 127, 0)], [(72, 127, 0)], [(74, 127, 0)],
                           [(75, 127, 0)], [(76, 127, 0)]],
        [[(79, 126, -1), (73, 2, 5), (80, 15, 7)], [(73, 1, 0), (82, 127, 1)],
         [(83, 120, -3), (81, 32, -1), (84, 31, 5)], [(85, 127, 0)], [(86, 127, 0)], [(87, 127, 0)], [(88, 127, 0)],
         [(90, 127, 0)]]]

    @staticmethod
    def get_effect_status(data, effect: int) -> bool:
        position = ZoomG3v2Patch.effects_status[effect]

        return (data[position + 4] & 0b00000001) == 0b00000001

    @staticmethod
    def get_effect(builder, data, effect: int) -> ZoomEffect:
        position = ZoomG3v2Patch.effects_status[effect]
        index = data[position + 4] >> 1

        return builder.build_by_id(index)

    @staticmethod
    def get_param(data, id_effect, id_param):
        params_data = ZoomG3v2Patch.params_bits[id_effect][id_param]

        value = 0
        for position, mask, shift in params_data:
            value |= shift_bits(data[position] & mask, shift)

        return value
