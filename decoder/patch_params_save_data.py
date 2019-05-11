import time

from decoder.params_by_position import params_with_max_value_by_position
from zoom.observer.zoom_host import ZoomHost
from zoom.zoomg3v2 import ZoomG3v2

# (name, id, max_value)
effects_per_param = params_with_max_value_by_position()
TIME_WAIT = 7


zoom = ZoomG3v2()
zoom.connect(ZoomHost())

time.sleep(1)

with open("decoder/data_params.csv", "w+") as file:
    zoom.host.host.connection.callback = lambda msg: file.write(str(msg.data).replace('(', '').replace(')', '') + '\n')

    for effect in range(6):
        for param, (_, effect_id, max_param_value) in enumerate(effects_per_param):
            file.write(f'{effect}, {param}\n')

            zoom.host.host.connection.send(zoom.host.host.message_encoder.set_effect(effect, effect_id))

            zoom.host.host.connection.send(zoom.host.host.message_encoder.set_param(effect, param, 0))
            time.sleep(TIME_WAIT)
            zoom.load_data()

            print(f'EFFECT {effect} PARAM {param}')
            for i in range(20):
                if 2**i > max_param_value:
                    break
                zoom.host.host.connection.send(zoom.host.host.message_encoder.set_param(effect, param, 2**i))
                time.sleep(TIME_WAIT)
                zoom.load_data()
