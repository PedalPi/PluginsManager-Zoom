import pdb
from time import sleep

from mido import Message

from zoom.observer.zoom_host import ZoomHost
from zoom.zoomg3v2 import ZoomG3v2
zoom = ZoomG3v2()
zoom.connect(ZoomHost())
zoom.load_data()


def write_data(msg: Message):
    if msg.type != 'sysex':
        return

    print(str(msg.data).replace('(', '').replace(')', ''))


for effect in range(6):
    zoom.host.host.connection.send(zoom.host.host.message_encoder.set_effect(effect, 0))
    for j in range(9):
        zoom.host.host.connection.send(zoom.host.host.message_encoder.set_param(effect, param_position=j, new_value=0))

zoom.host.host.connection.callback = write_data
zoom.load_data()

pdb.set_trace()

# Debug here
sleep(10)
