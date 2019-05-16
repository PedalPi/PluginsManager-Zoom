import time

from mido import Message

from decoder.lib.params_by_position import params_with_max_value_by_position
from zoom.observer.zoom_host import ZoomHost
from zoom.zoomg3v2 import ZoomG3v2

# (name, id, max_value)
effects_per_param = params_with_max_value_by_position()
TIME_WAIT = 10


zoom = ZoomG3v2()
zoom.connect(ZoomHost())

time.sleep(1)


def write_data(msg: Message):
    if msg.type != 'sysex':
        return

    file.write(str(msg.data).replace('(', '').replace(')', '') + '\n')


with open("decoder/data_params_3.csv", "w+") as file:
    zoom.host.host.connection.callback = write_data

    for effect in range(4, 6):
        for param, (_, effect_id, max_param_value) in enumerate(effects_per_param):
            time.sleep(TIME_WAIT)
            print(f'EFFECT {effect} PARAM {param}')
            file.write(f'{effect}, {param}\n')

            zoom.host.host.connection.send(zoom.host.host.message_encoder.set_effect(effect, effect_id))
            time.sleep(TIME_WAIT)

            for value in [0] + [2**i for i in range(20) if 2**i < max_param_value]:
                zoom.host.host.connection.send(zoom.host.host.message_encoder.set_param(effect, param, value))
                time.sleep(TIME_WAIT)
                zoom.load_data()

    # Don't close connection before register last command
    time.sleep(TIME_WAIT*5)
