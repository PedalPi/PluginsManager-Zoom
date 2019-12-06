from time import sleep

from pluginsmanager.model.effect import Effect
from pluginsmanager.observer.host_observer.host_observer import HostObserver
from pluginsmanager.observer.update_type import UpdateType

from zoom.observer.host.zoom_equipment_host import ZoomEquipmentHost, ZoomEquipmentHostData
from zoom.observer.zoom_change import ZoomChange


class ZoomHost(HostObserver):
    """
    For security, changes will be applied over the current pedalboard
    """

    def __init__(self, equipment_host: ZoomEquipmentHostData):
        super().__init__()
        context = ZoomHostContext(self)
        self.host = ZoomEquipmentHost(context, equipment_host)
        self.model: 'ZoomEquipment' = None

    def start(self):
        """
        Invokes the process.
        """
        pass

    def connect(self, model):
        """
        Connect with the host
        """
        self.model = model
        self.host.initialize()

    def close(self):
        """
        Remove the audio plugins loaded and closes connection with the host.
        """
        super().close()
        self.host.close()

    def load_data(self):
        for i in range(self.model.total_pedalboards):
            sleep(0.04)
            self.host.connection.send(self.host.message_encoder.specified_patch_details(i))

        self.host.connection.send(self.host.message_encoder.current_patch_number())

    # FIXME - on_current_pedalboard_changed
    # FIXME - on_pedalboard_updated
    def on_bank_updated(self, bank, update_type, **kwargs):
        # Do nothing
        pass

    def on_effect_updated(self, effect, update_type, index, origin, **kwargs):
        if origin != self.pedalboard:
            return

        # Create and delete make no sense
        if update_type == UpdateType.UPDATED:
            self._replace_effect(effect)
            self._load_params_of(effect)
            self.on_effect_status_toggled(effect)

    def on_custom_change(self, identifier, *args, **kwargs):
        print("Custom Change", identifier, args, kwargs)

        if identifier == ZoomChange.PEDALBOARD_CURRENT_LEVEL:
            pedalboard = args[0]
            self.host.connection.send(self.host.message_encoder.set_current_pedalboard_level(pedalboard.level))

        elif identifier == ZoomChange.PEDALBOARD_CURRENT:
            pedalboard, index = args
            self.host.connection.send(self.host.message_encoder.to_patch(index))

    def _replace_effect(self, effect):
        message = self.host.message_encoder.set_effect(effect.index, effect.plugin['id'])
        self.host.connection.send(message)

    def _add_effect(self, effect):
        # Do nothing
        pass

    def _remove_effect(self, effect):
        # Do nothing
        pass

    def _connect(self, connection):
        # Do nothing
        pass

    def _disconnect(self, connection):
        # Do nothing
        pass

    def _set_param_value(self, param):
        message = self.host.message_encoder.set_param(param.effect.index, param.index, param.value)
        self.host.connection.send(message)

    def _set_effect_status(self, effect: Effect):
        message = self.host.message_encoder.effect_status(effect.index, effect.active)
        self.host.connection.send(message)


class ZoomHostContext:

    def __init__(self, host: ZoomHost):
        self._host = host

    def __enter__(self) -> 'ZoomEquipment':
        self._host.__enter__()
        return self._host.model

    def __exit__(self, type, value, traceback):
        self._host.__exit__(type, value, traceback)
