from pluginsmanager.observer.updates_observer import UpdatesObserver

from zoom.observer.zoom_host import ZoomHost
from zoom.zoomg3v2 import ZoomG3v2


class Observer(UpdatesObserver):

    def on_bank_updated(self, *args, **kwargs):
        print('on_bank_updated', args, kwargs)

    def on_pedalboard_updated(self, pedalboard, update_type, index, origin, **kwargs):
        print('on_pedalboard_updated', pedalboard, update_type, index) #, args, kwargs
        pass

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


zoom = ZoomG3v2()
zoom.connect()
zoom.register(Observer())

zoom.load_data()

print('debug here')

zoom.disconnect()
