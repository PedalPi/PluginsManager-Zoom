from unittest.mock import MagicMock


class Effect(object):
    """
    Representation of a audio plugin instance.

    Effect contains a `active` status (off=bypass) and a list of :class:`Param`::

        >>> buidler = ZoomGSeriesBuilder()
        >>> amp = builder.build('MS 1959')
        >>> pedalboard.append(amp)
        >>> amp
        <Effect object as 'MS 1959' active at 0x7fd58d874ba8>

        >>> amp.active
        True
        >>> amp.toggle
        >>> amp.active
        False
        >>> amp.active = True
        >>> amp.active
        True

        >>> amp.params
        (<Param object 'Gain' as value=100 [0 - 100] at 0x7fdc96fc92e8>, <Param object 'Tube' as value=100 [0 - 100] at 0x7fdc96fcc3c8>, <Param object 'Level' as value=150 [0 - 150] at 0x7fdc96fce4a8>, <Param object 'Trebl' as value=100 [0 - 100] at 0x7fdc96fd0588>, <Param object 'Middl' as value=100 [0 - 100] at 0x7fdc96fd3668>, <Param object 'Bass' as value=100 [0 - 100] at 0x7fdc96fd5748>, <Param object 'Prese' as value=100 [0 - 100] at 0x7fdc96fd7860>, <Param object 'CAB' as value=22 [0 - 22] at 0x7fdc96fda978>)

    :param string name: Effect name.
    """

    def __init__(self, name):
        self.pedalboard = None

        self._name = name
        self._active = True

        self._params = ()

        self._observer = MagicMock()

    @property
    def observer(self):
        return self._observer

    @observer.setter
    def observer(self, observer):
        self._observer = observer

        for param in self.params:
            param.observer = self.observer

    @property
    def name(self):
        """
        :return string: Effect name
        """
        return self._name

    @property
    def params(self):
        """
        :return list[Param]: Params of effect
        """
        return self._params

    @property
    def active(self):
        """
        Effect status: active or bypass

        :getter: Current effect status
        :setter: Set the effect Status
        :type: bool
        """
        return self._active

    @active.setter
    def active(self, status):
        if status == self._active:
            return

        self._active = status
        self.observer.on_effect_status_toggled(self)

    def toggle(self):
        """
        Toggle the effect status: ``self.active = not self.active``
        """
        self.active = not self.active

    @property
    def json(self):
        """
        Get a json decodable representation of this effect

        :return dict: json representation
        """
        return self.__dict__

    @property
    def __dict__(self):
        return {
            'technology': 'zoomg3v2',
            'plugin': self.name,
            'active': self.active,
            'params': [param.json for param in self.params],
        }

    @property
    def index(self):
        """
        Returns the first occurrence of the effect in your pedalboard
        """
        if self.pedalboard is None:
            raise IndexError('Effect not contains a pedalboard')

        return self.pedalboard.effects.index(self)

    def __repr__(self, *args, **kwargs):
        return "<{} object as value='{}' {} at 0x{:x}>".format(
            self.__class__.__name__,
            self.name,
            'active' if self.active else 'disabled',
            id(self)
        )
