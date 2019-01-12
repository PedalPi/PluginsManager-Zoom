from pluginsmanager.model.param import Param
from pluginsmanager.model.effect import Effect

import json
import os

from pluginsmanager.util.dict_tuple import DictTuple


class ZoomGSeriesBuilder:

    def __init__(self):
        folder = os.path.dirname(os.path.realpath(__file__))
        self.filename = folder + '/database/ZoomG3v2.json'
        self.data = self._load(self.filename)

    def _load(self, filename):
        with open(filename) as data_file:
            return json.load(data_file)

    def build(self, plugin):
        plugin_data = self.data[plugin]

        effect = Effect(plugin_data['name'])
        params = []

        for param in plugin_data['parameters']:
            labels = param['labels'] if 'labels' in param else None

            params.append(Param(
                effect,
                param['name'],
                param['min'],
                param['max'],
                param['default'],
                labels
            ))

        effect._params = DictTuple(params, lambda param: param.symbol)

        return effect
