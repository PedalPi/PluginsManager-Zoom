import time

from mido import Message

from zoom.observer.zoom_host import ZoomHost
from zoom.zoomg3v2 import ZoomG3v2

TIME_WAIT = 10
max_level = 120

zoom = ZoomG3v2()
zoom.connect(ZoomHost())

time.sleep(1)


def write_data(msg: Message):
    if msg.type != 'sysex':
        return

    file.write(str(msg.data).replace('(', '').replace(')', '') + '\n')


with open("../../decoder/data_volume.csv", "w+") as file:
    zoom.host.host.connection.callback = write_data

    for value in [0] + [2**i for i in range(20) if 2**i < max_level]:
        zoom.host.host.connection.send(zoom.host.host.message_encoder.set_current_pedalboard_level(level=value))
        time.sleep(TIME_WAIT)
        zoom.host.host.connection.send(zoom.host.host.message_encoder.current_patch_details())

    # Don't close connection before register last command
    time.sleep(TIME_WAIT*5)
