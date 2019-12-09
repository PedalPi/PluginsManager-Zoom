import warnings
from typing import Collection

import mido

from zoom.observer.host.base.zoom_equipment_message_encoder import ZoomEquipmentMessageEncoder, \
    NotImplementedWarning


class ZoomIVMessageEncoder(ZoomEquipmentMessageEncoder):
    """
    Message encoder to Zoom ZFX-IV processor

    Based on:
     - https://www.vguitarforums.com/smf/index.php?topic=4329.msg131444#msg131444
     - https://github.com/sixeight7/VController_v2/blob/b435c733c6b174befad1c612ca5ddc1cb0168bca/VController_v2/MIDI_ZG3.ino

    Thanks sixeight7!
    """

    def set_effect(self, effect_position: int, new_effect: int) -> Collection[mido.Message]:
        return [self._zoom_small(effect_position, new_effect, 0x01)]

    def set_current_pedalboard_level(self, level: int) -> Collection[mido.Message]:
        return [self.zoom_sysex([0x31, 0x06, 0x02, level, 0])]

    #######################
    # Other configurations
    #######################
    def set_tempo(self, new_value: int) -> Collection[mido.Message]:
        return [self._zoom_small(0x06, new_value, 0x08)]

    def tuner(self, on: bool, bypass=None) -> Collection[mido.Message]:
        if bypass is not None:
            warnings.warn("bypass parameter only work with None value. Not implemented for other values", NotImplementedWarning)
            return []

        status_number = 0x64 if on else 0
        return [mido.Message('control_change', control=0x75, value=status_number)]


## Decode
# - Global -> AutoSave
# F0 52 00 5A 31 06 0A 00 00 F7
# F0 52 00 5A 31 06 0A 01 00 F7
# - Global -> Tempo
# F0 52 00 5A 31 06 08 vl 00 F7
# Sig. Path
# F0 52 00 5A 31 06 09 00 00 F7
# F0 52 00 5A 31 06 09 01 00 F7

# - Total -> Name
# F0 52 00 5A 31 07 lt vl 00 F7
# lt - letra 0-9
# vl - valor caractere ASCII
# - Total -> Level
# F0 52 00 5A 31 06 02 vl 00 F7
# - Total swap
# - Total CTRL SW/PDL (ControlSwitch/PDL)
# F0 52 00 5A 31 06 06 vl 00 F7
# vl - [00-08]
# - Total -> PDL DST -> 1° param - Assign
# - Total -> PDL DST -> 2° param - Aberto
# F0 52 00 5A 31 06 04 vl 00 F7
# vl - Depende do primeiro parâmetro
# - Total -> PDL DST -> 3° param - Fechado
# F0 52 00 5A 31 06 05 vl 00 F7
# vl - Depende do primeiro parâmetro

# - Store -> Store
# F0 52 00 5A 32 01 00 00 5F 00 00 00 00 00 F7
# - Store -> Swap
# F0 52 00 5A 32 02 00 00 5F 00 00 60 00 00 F7

# Ativar efeito - Comando grande
# Desativar - F0 52 00 5A 31 [effect] 00 00 00 F7
# Trocar efeito - Comando grande
# Trocar de banco - Comando Pequeno (CC 00, CC 32, PC [patch number])
# Alterar parâmetro - Comando Grande
