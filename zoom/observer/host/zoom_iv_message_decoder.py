from pluginsmanager.banks_manager import BanksManager

from zoom.model.zoom_pedalboard import ZoomPedalboard
from zoom.observer.host.protocol import MidiProtocol
from zoom.observer.host.zoomg3v2_patch import ZoomG3v2Patch
from zoom.observer.zoom_change import ZoomChange
from zoom.zoom_builder import ZoomBuilder


class ZoomIVMessageDecoder:

    def __init__(self, update_model):
        self.update_model = update_model

    def decode(self, message):
        if message.type == 'program_change':
            self.update_model(current_patch_id=+message.program)

        elif len(message) == 110:
            print('Current patch', message)

        elif len(message) == 120:
            self.update_model(pedalboard=self.decode_specific_path(message))

        elif len(message) == 10:
            print('Small data', message.hex())
            code, value = self.decode_small_data(message)

            print('code, value', code, value)

            if code is not None:
                self.update_model(code=code, value=value)

        elif len(message) == 15:
            print('Device info', message.hex())
            print(MidiProtocol.device_identity_reply_decode(message.data))

        else:
            # Path saved in x position
            # F0 52 00 5A 32 01 00 00 xx 00 00 00 00 00 F7
            # Swap xx <--> yy
            # F0 52 00 5A 32 02 00 00 xx 00 00 yy 00 00 F7
            print(message, '\n', message.hex())
            print('Size', len(message))

    def decode_specific_path(self, message):
        builder = ZoomBuilder(None)

        manufacturing_id = message.data[0]
        device_id = message.data[1]
        model_number = message.data[2]

        command_number = message.data[3]  # 08

        name = bytes(message.data[0x65:0x69] + message.data[0x6A:0x70]).decode()

        pedalboard = ZoomPedalboard(name=name)

        for id_effect in range(6):
            effect = ZoomG3v2Patch.get_effect(builder, message.data, id_effect)
            effect.active = ZoomG3v2Patch.get_effect_status(message.data[6:], id_effect)

            for id_param, param in enumerate(effect.params):
                param.value = ZoomG3v2Patch.get_param(message.data, id_effect, id_param)

            pedalboard.effects.append(effect)

        pedalboard.level = message.data[0x5c]

        # TODO: Display info
        # TODO: CTRL SW/PDL
        # TODO: PDL DST

        return pedalboard

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

        if type1 == 0x5A and type2 == 0x31 and type3 == ZoomChange.PEDALBOARD_CURRENT_LEVEL.value and type4 == 0x02:
            return ZoomChange.PEDALBOARD_CURRENT_LEVEL, value1

        return None, None
