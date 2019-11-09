from time import sleep

from zoom.observer.zoom_host import ZoomHost
from zoom.zoomg3v2 import ZoomG3v2


# Instantiate
zoom = ZoomG3v2()
# Connect the object 'zoom' with the real equipment
zoom.connect(ZoomHost())

# Load all patches from the equipment
zoom.load_data()

sleep(2)

# Print current patch
print('Current pedalboard:', zoom.current_pedalboard)

# Toggle status
for effect in zoom.current_pedalboard.effects[0]:
    effect.toogle()
    sleep(1)

# Toggle status
for effect in zoom.current_pedalboard.effects[0]:
    effect.toogle()
    sleep(1)

# Go to next pedalboard
zoom.to_next_pedalboard()
sleep(2)
# Go to previous pedalboard
zoom.to_previous_pedalboard()
sleep(2)

# See all patches
print(zoom.banks[0].pedalboards)
