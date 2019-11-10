from time import sleep

from pluginsmanager.observer.updates_observer import UpdatesObserver

from zoom.observer.zoom_host import ZoomHost
from zoom.zoomg3v2 import ZoomG3v2


class Observer(UpdatesObserver):

    def on_bank_updated(self, *args, **kwargs):
        print('on_bank_updated', args, kwargs)

    def on_pedalboard_updated(self, *args, **kwargs):
        print('on_pedalboard_updated', args, kwargs)

    def on_effect_updated(self, *args, **kwargs):
        print('on_effect_updated', args, kwargs)

    def on_effect_status_toggled(self, *args, **kwargs):
        print('on_effect_status_toggled', args, kwargs)

    def on_param_value_changed(self, *args, **kwargs):
        print('on_param_value_changed', args, kwargs)

    def on_connection_updated(self, *args, **kwargs):
        print('on_connection_updated', args, kwargs)

    def on_custom_change(self, *args, **kwargs):
        print('on_custom_change', args, kwargs)

# Instantiate
zoom = ZoomG3v2()
# Connect the object 'zoom' with the real equipment
zoom.connect(ZoomHost())
zoom.register(Observer())

# Load all patches from the equipment
zoom.load_data()

sleep(2)

# Print current patch
print('Current pedalboard:', zoom.current_pedalboard)

# Set level of current pedalboard
#zoom.current_pedalboard.level = 25
sleep(2)

# Toggle status
for effect in zoom.current_pedalboard.effects:
    effect.toggle()
    sleep(.5)

# Toggle status
for effect in zoom.current_pedalboard.effects:
    effect.toggle()
    sleep(.5)

# Go to next pedalboard
zoom.to_next_pedalboard()
sleep(2)
# Go to previous pedalboard
zoom.to_previous_pedalboard()
sleep(2)

# See all patches
print(zoom.pedalboards)
