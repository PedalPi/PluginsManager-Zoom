import json
import os

from zoom.database import ZoomMSSeries
from zoom.model.zoom.zoom_effect import ZoomEffect
from zoom.zoom_model import ZoomModel


class ZoomEffectsBuilder:
    """
    Generate the audio plugins based in the equipment
    """

    def __init__(self, model: ZoomModel):
        folder = os.path.dirname(os.path.realpath(__file__))

        if model == ZoomModel.ZoomG3v2:
            filename = folder + '/database/ZoomG3v2.json'
            self.data = self._load(filename)
            self._index_and_names = {v['id']: k for k, v in self.data.items()}

        elif model == ZoomModel.ZoomMS50g:
            self.data = ZoomMSSeries.effectlist
            self._index_and_names = {k: v['name'] for k, v in self.data.items()}

    def _load(self, filename: str) -> dict:
        with open(filename) as data_file:
            return json.load(data_file)

    def build_by_id(self, index: int) -> ZoomEffect:
        return self.build_by_name(self._name_by_index(index))

    def _name_by_index(self, index) -> str:
        return self._index_and_names[index]

    def build_by_name(self, name: str) -> ZoomEffect:
        plugin_data = self.data[name]

        return ZoomEffect(plugin_data)
