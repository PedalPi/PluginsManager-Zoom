from time import sleep

from pluginsmanager.model.effect import Effect
from pluginsmanager.observer.host_observer.host_observer import HostObserver

from zoom.observer.host.zoom_iv_host import ZoomIVHost


class ZoomHost(HostObserver):
    """
    For security, changes will be applied over the current pedalboard
    """

    def __init__(self):
        super().__init__()
        self.host = ZoomIVHost(lambda **kwargs: self.update_model(**kwargs))
        self.model = None

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
        for i in range(100):
            sleep(0.03)
            self.host.connection.send(self.host.message_encoder.specified_patch_details(i))

        self.host.connection.send(self.host.message_encoder.current_patch_number())

    def update_model(self, current_patch_id=None, pedalboard=None):
        with self:
            if current_patch_id is not None:
                self.model.to_pedalboard(current_patch_id)
            elif pedalboard is not None:
                self.model.pedalboards.append(pedalboard)

    def _add_effect(self, effect):
        pass

    def _remove_effect(self, effect):
        pass

    def _connect(self, connection):
        # Do nothing
        pass

    def _disconnect(self, connection):
        # Do nothing
        pass

    def _set_param_value(self, param):
        pass

    def _set_effect_status(self, effect: Effect):
        self.host.connection.send(self.host.message_encoder.effect_status(effect.index, effect.active))
