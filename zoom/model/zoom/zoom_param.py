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
    def values(self):
        """
        :return: All the possible values. Use this method when a parameter is a categorical parameter.
        """
        if self.categorical:
            return self.data['values']

        return range(self.minimum, self.maximum+1)

    @property
    def categorical(self):
        """
        Some parameters have categorical values. In these there is a descriptive representation associated with the
        value.
        This descriptive representation is the one commonly presented in programs and on the equipment itself.

        :return: This parameter is categorical?
        """
        return 'values' in self.data

    @property
    def symbol(self):
        return self.data['name']

    @property
    def label(self):
        """
        Some parameters have categorical values. In these there is a descriptive representation associated with the
        value.
        This descriptive representation is the one commonly presented in programs and on the equipment itself.

        :return: The descriptive representation (label) of the current param value
        """
        return self.labels[self.value]

    @property
    def labels(self):
        """
        Some parameters have categorical values. In these there is a descriptive representation associated with the
        value.
        This descriptive representation is the one commonly presented in programs and on the equipment itself.

        :return: The descriptive representations (labels) of the all param value
        """
        return self._labels

    def __str__(self):
        return f"{self.symbol}: {self.label} [{self.labels[self.minimum]}, {self.labels[self.maximum]}]"

    def __repr__(self):
        return self.__str__()
