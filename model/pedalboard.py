from util.observable_list import ObservableList
from model.update_type import UpdateType

from unittest.mock import MagicMock


class Pedalboard(object):
    """
    Pedalboard is a patch representation: your structure contains
    :class:`Effect`::

        >>> pedalboard = Pedalboard('Rocksmith')
        >>> bank.append(pedalboard)

        >>> builder = Lv2EffectBuilder()
        >>> pedalboard.effects
        ObservableList: []
        >>> reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        >>> pedalboard.append(reverb)
        >>> pedalboard.effects
        ObservableList: [<Lv2Effect object as 'Calf Reverb'  active at 0x7f60effb09e8>]

        >>> fuzz = builder.build('http://guitarix.sourceforge.net/plugins/gx_fuzzfacefm_#_fuzzfacefm_')
        >>> pedalboard.effects.append(fuzz)

        >>> pedalboard.data
        {}
        >>> pedalboard.data = {'my-awesome-component': True}
        >>> pedalboard.data
        {'my-awesome-component': True}

    For load the pedalboard for play the songs with it::

        >>> mod_host.pedalboard = pedalboard

    All changes¹ in the pedalboard will be reproduced in mod-host.
    ¹ Except in data attribute, changes in this does not interfere with anything.

    :param string name: Pedalboard name
    """
    def __init__(self, name):
        self.name = name
        self._effects = ObservableList()

        self.effects.observer = self._effects_observer

        self._observer = MagicMock()

        self.bank = None

        self.data = {}

    @property
    def observer(self):
        return self._observer

    @observer.setter
    def observer(self, observer):
        self._observer = observer

        for effect in self.effects:
            effect.observer = observer

    def _effects_observer(self, update_type, effect, index):
        kwargs = {
            'index': index,
            'origin': self
        }

        if update_type == UpdateType.CREATED \
        or update_type == UpdateType.UPDATED:
            effect.pedalboard = self
            effect.observer = self.observer
        elif update_type == UpdateType.DELETED:
            effect.pedalboard = None
            effect.observer = MagicMock()

        self.observer.on_effect_updated(effect, update_type, **kwargs)

    @property
    def json(self):
        """
        Get a json decodable representation of this pedalboard

        :return dict: json representation
        """
        return self.__dict__

    @property
    def __dict__(self):
        return {
            'name': self.name,
            'effects': [effect.json for effect in self.effects],
            'data': self.data
        }

    def append(self, effect):
        """
        Add a :class:`Effect` in this pedalboard

        This works same as::

            >>> pedalboard.effects.append(effect)

        or::

            >>> pedalboard.effects.insert(len(pedalboard.effects), effect)

        :param Effect effect: Effect that will be added
        """
        self.effects.append(effect)

    @property
    def effects(self):
        """
        Return the effects presents in the pedalboard

        .. note::

            Because the effects is an :class:`ObservableList`, it isn't settable.
            For replace, del the effects unnecessary and add the necessary
            effects
        """
        return self._effects

    @property
    def index(self):
        """
        Returns the first occurrence of the pedalboard in your bank
        """
        if self.bank is None:
            raise IndexError('Pedalboard not contains a bank')

        return self.bank.pedalboards.index(self)
