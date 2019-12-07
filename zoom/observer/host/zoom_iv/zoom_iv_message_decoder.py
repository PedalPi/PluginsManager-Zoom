from zoom.model.zoom_pedalboard import ZoomPedalboard
from zoom.observer.host.protocol import MidiProtocol

from zoom.observer.host.zoom_iv.zoomg3v2_patch_decoder import ZoomG3v2PatchDecoder
from zoom.observer.zoom_change import ZoomChange

from zoom.zoom_model import ZoomModel


class ZoomIVMessageDecoder:

    def __init__(self, context):
        self._context = context

    def decode(self, message):
        print(len(message), message)

        if message.type == 'program_change':
            with self._context as model:
                model.to_pedalboard(+message.program)

        elif len(message) == 10:
            self.decode_small_data(message)

        elif len(message) == 15:
            print('Device info', message.hex())
            print(MidiProtocol.device_identity_reply_decode(message.data))

        # Update current pedalboard
        elif len(message) == 110:
            with self._context as model:
                current_pedalboard = model.current_pedalboard
                ZoomG3v2PatchDecoder().decode(message.data, current_pedalboard)

        # Update specific pedalboard
        # FIXME - Ever add the pedalboard?!!
        elif len(message) == 120:
            pedalboard = ZoomG3v2PatchDecoder().decode(message.data, ZoomPedalboard(""))
            with self._context as model:
                model.pedalboards.append(pedalboard)

        else:
            # Path saved in x position
            # F0 52 00 5A 32 01 00 00 xx 00 00 00 00 00 F7
            # Swap xx <--> yy
            # F0 52 00 5A 32 02 00 00 xx 00 00 yy 00 00 F7
            print("Not mapped")
            print(message, '\n', message.hex())
            print('Size', len(message))

    def decode_small_data(self, message):
        # Commands (F0 52 00 5A xx)
        # 08: Specific path
        # 28: Current path / Foot switch expression
        # 31: Global info: Tempo / Signal path / Auto save / Foot switch (min, max)
        # 31: Patch info: Patch name / Patch volume / Ctrl switch assignment
        # 31: Effect param value:
        # 32: Patch saved
        type1 = message.data[0x02]
        type2 = message.data[0x03]
        type3 = message.data[0x04]
        type4 = message.data[0x05]
        value1 = message.data[0x06]
        value2 = message.data[0x07]

        if type1 != ZoomModel.ZoomG3v2.value:
            return

        # Pedalboard level
        if type2 == 0x31 and type3 == ZoomChange.PEDALBOARD_CURRENT_LEVEL.value and type4 == 0x02:
            with self._context as model:
                model.current_pedalboard.level = value1

        # Pedalboard name
        elif type2 == 0x31 and type3 == ZoomChange.PEDALBOARD_NAME.value and (0x00 <= type4 <= 0x09):
            with self._context as model:
                pos = type4
                new_letter = bytes([value1]).decode()
                name = model.current_pedalboard.name
                new_name = name[:pos] + new_letter + name[pos+1:]

                model.current_pedalboard.name = new_name

        # Param value
        elif type2 == 0x31 and (0x00 <= type3 <= 0x05):
            id_effect = type3

            if 0x00 == type4:
                with self._context as model:
                     model.current_pedalboard.effects[id_effect].active = False

            elif 0x02 <= type4 <= 0x09:
                id_param = type4 - 2
                value = (value2 << 7) + value1

                with self._context as model:
                    model.current_pedalboard.effects[id_effect].params[id_param].value = value

        print(hex(type1), hex(type2), hex(type3), hex(type4))
