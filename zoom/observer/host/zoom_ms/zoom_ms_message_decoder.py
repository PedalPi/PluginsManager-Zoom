from zoom.model.zoom_pedalboard import ZoomPedalboard
from zoom.observer.host.protocol import MidiProtocol
from zoom.observer.host.zoom_ms.zoom_ms_patch_decoder import ZoomMSPatchDecoder
from zoom.zoom_model import ZoomModel


class ZoomMSMessageDecoder:

    def __init__(self, context):
        self._context = context

    def decode(self, message):
        print(len(message), message)

        if message.type == 'program_change':
            with self._context as model:
                model.to_pedalboard(+message.program)

        elif len(message) == 15:
            print('Device info', message.hex())
            print(MidiProtocol.device_identity_reply_decode(message.data))

        elif len(message) == 10:
            self.decode_small_data(message)

        # Update current pedalboard
        elif len(message) == 146:
            with self._context as model:
                current_pedalboard = model.current_pedalboard
                ZoomMSPatchDecoder().decode(message.data, current_pedalboard)

        # Update specific pedalboard
        # FIXME - Ever add the pedalboard?!!
        elif len(message) == 156:
            data = message.data[5:]

            pedalboard = ZoomMSPatchDecoder().decode(data, ZoomPedalboard(""))
            with self._context as model:
                model.pedalboards.append(pedalboard)

        else:
            print("Not mapped")
            print(message, '\n', message.hex())
            print('Size', len(message))

    def decode_small_data(self, message):
        type1 = message.data[0x02]
        type2 = message.data[0x03]
        type3 = message.data[0x04]
        type4 = message.data[0x05]
        value1 = message.data[0x06]
        value2 = message.data[0x07]

        if type1 != ZoomModel.ZoomMS50g.value:
            return

        if type2 == 0x31 and (0x00 <= type3 <= 0x05):
            id_effect = type3

            # Effect status
            if 0x00 == type4:
                with self._context as model:
                     model.current_pedalboard.effects[id_effect].active = False

            # Param value
            elif 0x02 <= type4 <= 0x10:
                id_param = type4 - 2
                value = (value2 << 7) + value1

                with self._context as model:
                    model.current_pedalboard.effects[id_effect].params[id_param].value = value

        print(hex(type1), hex(type2), hex(type3), hex(type4))
