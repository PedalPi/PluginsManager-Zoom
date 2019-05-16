import time

from mido import Message

from zoom.observer.zoom_host import ZoomHost
from zoom.zoomg3v2 import ZoomG3v2

TIME_WAIT = 8


zoom = ZoomG3v2()
zoom.connect(ZoomHost())

time.sleep(1)


def write_data(msg: Message):
    if msg.type != 'sysex':
        return

    file.write(str(msg.data).replace('(', '').replace(')', '') + '\n')


with open("decoder/data_effects.csv", "w+") as file:
    zoom.host.host.connection.callback = write_data

    for effect in range(6):
        print(f'EFFECT {effect}')
        file.write(f'{effect}\n')

        zoom.host.host.connection.send(zoom.host.host.message_encoder.set_effect(effect, 0))
        for j in range(9):
            zoom.host.host.connection.send(zoom.host.host.message_encoder.set_param(effect, param_position=j, new_value=0))
        time.sleep(TIME_WAIT)
        zoom.load_data()

        for i in range(7):
            zoom.host.host.connection.send(zoom.host.host.message_encoder.set_effect(effect, 2**i))
            for j in range(9):
                zoom.host.host.connection.send(zoom.host.host.message_encoder.set_param(effect, param_position=j, new_value=0))
            time.sleep(TIME_WAIT)
            zoom.load_data()
