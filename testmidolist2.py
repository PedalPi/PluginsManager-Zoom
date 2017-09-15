import sys
import mido
from signal import pause
from time import sleep

def start():
    if len(sys.argv) > 1:
        portname = sys.argv[1]
    else:
        portname = None  # Use default port

    with mido.open_input(portname) as port:
        port.callback = lambda a: print(a)
        pause()


class ZoomGSeries:

    def __init__(self):
        self.manufacturing_id = 0x52
        self.device_id = 0x00
        self.model_number = 0x5A

        self.name = 'ZOOM G Series MIDI 1'

        self.connection = Connection(self.name)
        self.connection.callback = lambda message: self.decode(message)
        self.message_encoder = ZoomGSeriesMessageEncoder(self.manufacturing_id, self.device_id, self.model_number)

    def initialize(self):
        device_info = mido.Message('sysex', data=[0x7E, 0x00, 0x06, 0x01])

        self.connection.send(device_info)
        self.connection.send(self.message_encoder.enable_editor())

    def close(self):
        self.connection.send(self.message_encoder.disable_editor())

    def zoom_sysex(self, data):
        head = [self.manufacturing_id, self.device_id, self.model_number]
        return mido.Message('sysex', data=head+data)

    def decode(self, message):
        if message.type == 'program_change':
            print('Current patch is', "'" + str(+message.program) + "'")

        elif len(message) == 110:
            print('Current patch', message)

        elif len(message) == 120:
            print('Specified patch', message)

        elif len(message) == 15:
            print('Device info', message)

        else:
            print(message, '\n', message.hex())
            print('Size', len(message))


class Connection(object):
    def __init__(self, port_name):
        self.name = port_name
        self.midiout = mido.open_output(self.name)
        self.midiin = mido.open_input(self.name)

    @property
    def callback(self):
        return self.midiin.callback

    @callback.setter
    def callback(self, callback):
        self.midiin.callback = callback

    def send(self, message):
        print(message.hex())
        self.midiout.send(message)


class ZoomGSeriesMessageEncoder(object):

    def __init__(self, manufacturing_id, device_id, model_number):
        self.manufacturing_id = manufacturing_id
        self.device_id = device_id
        self.model_number = model_number

    def zoom_sysex(self, data):
        head = [self.manufacturing_id, self.device_id, self.model_number]
        return mido.Message('sysex', data=head+data)

    #######################
    ## Enable/disable configuration
    #######################
    def enable_editor(self):
        return self.zoom_sysex([0x50])

    def disable_editor(self):
        return self.zoom_sysex([0x51])

    #######################
    ## Obtain patch details
    #######################
    def current_patch_number(self):
        return self.zoom_sysex([0x33])

    def current_patch_details(self):
        return self.zoom_sysex([0x29])

    def specified_patch_details(self, number):
        return self.zoom_sysex([0x09, 0x00, 0x00, number])

    #######################
    ## Effect and Param
    #######################
    def effect_on(self, position):
        return self.effect_status(position, True)

    def effect_off(self, position):
        return self.effect_status(position, False)

    def effect_status(self, position, status):
        status_number = 1 if status else 0
        return self._zoom_small(position, status_number, 0x00)

    def set_effect(self, effect_position, new_effect):
        return self._zoom_small(effect_position, new_effect, 0x01)

    def set_param(self, effect_position, param_position, new_value):
        return self._zoom_small(effect_position, new_value, param_position + 0x02)

    def _zoom_small(self, position, value, effect_message_type):
        """
        :param position:
        :param value:
        :param effect_message_type:
                     0 - Effect status
                     1 - Set effect
                     [2..7] - Set param value
        :return:
        """
        value2 = 0
        if value >= 128:
            value -= 128
            value2 = 0b00000001

        return self.zoom_sysex([0x31, position, effect_message_type, value, value2])

    #######################
    ## Pedalboard
    #######################
    def to_patch(self, number):
        return mido.Message('program_change', channel=0x00, program=number)

    #######################
    ## Other configurations
    #######################
    def set_tempo(self, new_value):
        return self._zoom_small(0x06, new_value, 0x08)

    def set_tempo(self, new_value):
        return self._zoom_small(0x06, new_value, 0x08)

    #######################
    ## ???
    #######################
    def tuner_bypass(self, status):
        status_number = 0x64 if status else 0
        return mido.Message('control_change', control=0x75, value=status_number)

    def tuner_mute_off(self):
        return mido.Message('control_change', control=0x75, value=0x00)

    def tuner_mute_on(self):
        return mido.Message('control_change', control=0x75, value=0x64)

    def deprecated_you_can_talk(self):
        return self.zoom_sysex([16])

def tratar_mensagem(mensagem):
    '''
    [f0 52 00 5a 28 50 0c 00
     00 02 00 00 00 02 64 00

     00 00 00 0a 00 40 00 02
     00 00 00 64 00 02 00 00

     00 2e 0c 00 01 00 20 03
     00 00 00 00 00 20 00 56

     00 00 00 00 00 01 00 00
     00 00 00 00 56 00 00 00

     00 00 00 00 00 04 00 00
     00 00 56 00 00 00 00 00

     00 00 00 00 00 00 00 00
     64 00 1c 00 00 20 00 40

     58 20 20 20 20 00 20 20
     20 20 20 20 00 f7]
    '''
    range(5, 110, 8)

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


zoom_g3 = ZoomGSeries()
zoom_g3.initialize()

zoom_g3.connection.send(zoom_g3.message_encoder.deprecated_you_can_talk())
sleep(1)

'''
# Current Data
sleep(1)
zoom_g3.connection.send(zoom_g3.message_encoder.current_patch_number())

sleep(1)
zoom_g3.connection.send(zoom_g3.message_encoder.current_patch_details())

sleep(1)
zoom_g3.connection.send(zoom_g3.message_encoder.specified_patch_details(00))
'''
# Effect
sleep(1)
zoom_g3.connection.send(zoom_g3.message_encoder.effect_on(1))
sleep(1)
zoom_g3.connection.send(zoom_g3.message_encoder.effect_off(1))

'''
# Set Patch
zoom_g3.connection.send(zoom_g3.message_encoder.to_patch(00))
sleep(1)
zoom_g3.connection.send(zoom_g3.message_encoder.to_patch(95))
sleep(1)
'''

'''
# Tuner
zoom_g3.connection.send(zoom_g3.message_encoder.tuner_bypass(True))
sleep(1)

zoom_g3.connection.send(zoom_g3.message_encoder.tuner_bypass(False))
sleep(1)
'''

'''
# Set Effect
zoom_g3.connection.send(zoom_g3.message_encoder.set_effect(0, 25))
sleep(1)
zoom_g3.connection.send(zoom_g3.message_encoder.set_effect(0, 3))
sleep(1)

# Set Param value
zoom_g3.connection.send(zoom_g3.message_encoder.set_param(2, 2, 15))
sleep(1)

zoom_g3.connection.send(zoom_g3.message_encoder.set_param(2, 2, 150))
sleep(1)

# Set tempo
zoom_g3.connection.send(zoom_g3.message_encoder.set_tempo(150))
sleep(1)

zoom_g3.connection.send(zoom_g3.message_encoder.set_tempo(100))
sleep(1)
'''


#zoom_g3.close()

pause()
