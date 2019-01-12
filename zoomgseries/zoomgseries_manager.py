from pluginsmanager.observer.updates_observer import UpdatesObserver


class ZoomGSeriesObserver(UpdatesObserver):

    def on_bank_updated(self, bank, update_type, **kwargs):
        print(bank, update_type, kwargs)

    def on_pedalboard_updated(self, pedalboard, update_type, **kwargs):
        print(pedalboard, update_type, kwargs)

    def on_effect_updated(self, effect, update_type, **kwargs):
        print(effect, update_type, kwargs)

    def on_effect_status_toggled(self, effect, **kwargs):
        print(effect)

    def on_param_value_changed(self, param, **kwargs):
        print(param)

    def on_connection_updated(self, connection, update_type, pedalboard, **kwargs):
        pass
