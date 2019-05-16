import time

from mido import Message

from decoder.lib.params_by_position import params_with_max_value_by_position
from zoom.observer.zoom_host import ZoomHost
from zoom.zoomg3v2 import ZoomG3v2

# (name, id, max_value)
effects_per_param = params_with_max_value_by_position()
TIME_WAIT = 8


zoom = ZoomG3v2()
zoom.connect(ZoomHost())

time.sleep(1)


def write_data(msg: Message):
    if msg.type != 'sysex':
        return

    file.write(str(msg.data).replace('(', '').replace(')', '') + '\n')


with open("decoder/data_effects_status.csv", "w+") as file:
    zoom.host.host.connection.callback = write_data

    for effect in range(6):
        file.write(f'{effect}\n')
        zoom.host.host.connection.send(zoom.host.host.message_encoder.effect_off(effect))
        zoom.load_data()

        time.sleep(TIME_WAIT)

        zoom.host.host.connection.send(zoom.host.host.message_encoder.effect_on(effect))
        zoom.load_data()
