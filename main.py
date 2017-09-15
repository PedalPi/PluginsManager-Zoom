import rtmidi
import time
from signal import pause


class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        print(event, data)
        message, deltatime = event
        self._wallclock += deltatime
        print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))


midiout = rtmidi.MidiOut()
print(midiout.get_ports())
midiout.open_port(1)

midiout.send_message([0xF0, 0x52, 0x00, 0x5A, 0x33, 0xF7])
midiout.send_message([0xF0, 0x52, 0x00, 0x5A, 0x33, 0xF7])

midiin = rtmidi.MidiIn()
midiin.set_callback(MidiInputHandler('Teste Zoom'))
midiin.open_port(1)



try:
    pause()
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin
