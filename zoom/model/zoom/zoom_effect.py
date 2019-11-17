# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pluginsmanager.model.effect import Effect

from pluginsmanager.util.dict_tuple import DictTuple
from zoom.model.zoom.zoom_param import ZoomParam


class ZoomEffect(Effect):
    """
    Representation of a Zoom Effect audio plugin instance.

    The inputs and outputs are empty because the effects order defines
    the connections between effects
    """

    def __init__(self, plugin):
        super(ZoomEffect, self).__init__()

        self.plugin = plugin

        params = [ZoomParam(self, param) for param in plugin["parameters"]]
        self._params = DictTuple(params, lambda param: param.symbol)

        inputs = []
        self._inputs = DictTuple(inputs, lambda _input: _input.symbol)

        outputs = []
        self._outputs = DictTuple(outputs, lambda _output: _output.symbol)

        midi_inputs = []
        self._midi_inputs = DictTuple(midi_inputs, lambda _output: _output.symbol)

        midi_outputs = []
        self._midi_outputs = DictTuple(midi_outputs, lambda _output: _output.symbol)

        self.instance = None

    def __str__(self):
        return f"{self.plugin['name']} {'on' if self.active else 'off'} ({[param.__str__() for param in self.params]})"

    @property
    def __dict__(self):
        return {
            'technology': 'zoom-zfx',
            'plugin': self.plugin['name'],
            'active': self.active,
            'params': [param.json for param in self.params],
            'version': self.version
        }

    @property
    def version(self):
        """
        :return string: Version of plugin of effect
        """
        # FIXME
        return 'FIXME-ZoomG3v2'
