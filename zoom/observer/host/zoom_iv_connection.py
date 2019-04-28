import mido


class ZoomIVConnection(object):
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
