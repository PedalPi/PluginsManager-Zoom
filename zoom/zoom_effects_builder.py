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

        elif model == ZoomModel.ZoomMS50g:
            self.data = ZoomMSSeries.effectlist

        # Remove key string in json data
        self.data = {int(k): v for k, v in self.data.items()}
        # Enable to build by id
        self._name_by_id = {v['name']: k for k, v in self.data.items()}

    def _load(self, filename: str) -> dict:
        with open(filename) as data_file:
            return json.load(data_file)

    def build_by_id(self, index: int) -> ZoomEffect:
        return ZoomEffect(self.data[index])

    def build_by_name(self, name: str) -> ZoomEffect:
        index = self._name_by_id[name]
        return self.build_by_id(index)
