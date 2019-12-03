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

from pluginsmanager.model.param import Param


class ZoomParam(Param):
    """
    Representation of a Zoom `input control port`_ instance.

    For general input use, see :class:`.Param` class documentation.

    :param ZoomEffect effect: Effect that contains the param
    :param dict data: json representation
    """

    def __init__(self, effect, data):
        super().__init__(effect, data['default'])
        self._data = data
        self._labels = self.data['labels'] if 'labels' in self.data else range(self.minimum, self.maximum+1)

    @property
    def data(self):
        return self._data

    @property
    def maximum(self):
        return self.data['max']

    @property
    def minimum(self):
        return 0 if 'min' not in self.data else self.data['min']

    @property
    def symbol(self):
        return self.data['name']

    @property
    def label(self):
        return self.labels[self.value]

    @property
    def labels(self):
        return self._labels

    def __str__(self):
        return f"{self.symbol}: {self.label} [{self.labels[self.minimum]}, {self.labels[self.maximum]}]"
