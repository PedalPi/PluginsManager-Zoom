import time

from zoom.observer.zoom_host import ZoomHost
from zoom.zoomg3v2 import ZoomG3v2

TIME_WAIT = 7


zoom = ZoomG3v2()
zoom.connect(ZoomHost())

time.sleep(1)


with open("decoder/data_effects.csv", "w+") as file:
    def function(msg):
        if msg.type == 'sysex':
            file.write(str(msg.data).replace('(', '').replace(')', '') + '\n')

    zoom.host.host.connection.callback = function

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
