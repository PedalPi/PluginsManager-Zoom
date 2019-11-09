from pluginsmanager.observer.host_observer.host_observer import HostObserver

from zoom.observer.host.zoom_iv_host import ZoomIVHost


class ZoomHost(HostObserver):

    def __init__(self):
        super().__init__()
        self.host = ZoomIVHost()

    def start(self):
        """
        Invokes the process.
        """
        pass

    def connect(self):
        """
        Connect with the host
        """
        self.host.initialize()

    def close(self):
        """
        Remove the audio plugins loaded and closes connection with the host.
        """
        super().close()
        self.host.close()

    def load_data(self):
        self.host.connection.send(self.host.message_encoder.current_patch_number())

        for i in range(100):
            self.host.connection.send(self.host.message_encoder.specified_patch_details(i))
        #self.host.connection.send(self.host.message_encoder.specified_patch_details(98))

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

    def _set_effect_status(self, effect):
        pass