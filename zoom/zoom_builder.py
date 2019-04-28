import json
import os

from zoom.model.zoom.zoom_effect import ZoomEffect
from zoom.zoom_model import ZoomModel


class ZoomBuilder:

    def __init__(self, model: ZoomModel):
        folder = os.path.dirname(os.path.realpath(__file__))
        self.filename = folder + '/database/ZoomG3v2.json'
        self.data = self._load(self.filename)

    def _load(self, filename):
        with open(filename) as data_file:
            return json.load(data_file)

    def build(self, plugin):
        plugin_data = self.data[plugin]

        return ZoomEffect(plugin_data)
