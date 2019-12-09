from typing import Collection

import mido


class ZoomConnection(object):
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

    def send_all(self, messages: Collection[mido.Message]):
        for message in messages:
            self.send(message)

    def send(self, message: mido.Message):
        print('sent', message.hex())
        self.midiout.send(message)
