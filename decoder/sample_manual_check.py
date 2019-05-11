from time import sleep

from zoom.observer.zoom_host import ZoomHost
from zoom.zoomg3v2 import ZoomG3v2
zoom = ZoomG3v2()
zoom.connect(ZoomHost())
zoom.load_data()

# Debug here
sleep(10)
