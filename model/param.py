from unittest.mock import MagicMock


class ParamError(Exception):

    def __init__(self, message):
        super(ParamError, self).__init__(message)
        self.message = message


class Param(object):
    """
    :class:`Param` represents an Audio Plugin Parameter::

        >>> my_awesome_effect
        <Effect object as 'MS 1959' active at 0x7fd58d874ba8>
        >>> my_awesome_effect.params
        (<Param object 'Gain' as value=100 [0 - 100] at 0x7fdc96fc92e8>, <Param object 'Tube' as value=100 [0 - 100] at 0x7fdc96fcc3c8>, <Param object 'Level' as value=150 [0 - 150] at 0x7fdc96fce4a8>, <Param object 'Trebl' as value=100 [0 - 100] at 0x7fdc96fd0588>, <Param object 'Middl' as value=100 [0 - 100] at 0x7fdc96fd3668>, <Param object 'Bass' as value=100 [0 - 100] at 0x7fdc96fd5748>, <Param object 'Prese' as value=100 [0 - 100] at 0x7fdc96fd7860>, <Param object 'CAB' as value=22 [0 - 22] at 0x7fdc96fda978>)

        >>> param = my_awesome_effect.params[0]
        >>> param
        <Param object 'Gain' as value=100 [0 - 100] at 0x7fdc96fc92e8>

        >>> param.value = 14
        >>> param
        <Param object 'Gain' as value=14 [0 - 100] at 0x7fdc96fc92e8>

        >>> symbol = param.symbol
        >>> symbol
        'Gain'
        >>> param == my_awesome_effect.params[symbol]
        True

    :param Effect effect: Effect in which this parameter belongs
    :param string name: Param name
    :param int minimum: Smaller value that the parameter can assume
    :param int maximum: Greater value that the parameter can assume
    :param int initial_value: Initial value that the parameter will be assumed
    :param string[] labels: Labels for the possible values
    """

    def __init__(self, effect, name, minimum, maximum, initial_value, labels=None):
        self._effect = effect
        self._value = initial_value

        self._name = name
        self._minimum = minimum
        self._maximum = maximum

        self._labels = labels

        self.observer = MagicMock()

    @property
    def effect(self):
        """
        :return: Effect in which this parameter belongs
        """
        return self._effect

    @property
    def value(self):
        """
        Parameter value

        :getter: Current value
        :setter: Set the current value
        """
        return self._value

    @value.setter
    def value(self, new_value):
        if self._value == new_value:
            return

        if not(self.minimum <= new_value <= self.maximum):
            msg = 'New value out of range: {} [{} - {}]'.format(
                new_value,
                self.minimum,
                self.maximum
            )
            raise ParamError(msg)

        self._value = new_value
        self.observer.on_param_value_changed(self)

    @property
    def minimum(self):
        """
        :return: Smaller value that the parameter can assume
        """
        return self._minimum

    @property
    def maximum(self):
        """
        :return: Greater value that the parameter can assume
        """
        return self._maximum

    @property
    def labels(self):
        """
        :return string[]: Labels for the possible values
        """
        return self._labels

    @property
    def symbol(self):
        """
        :return: Param identifier
        """
        return self._name

    def __repr__(self, *args, **kwargs):
        return "<{} object '{}' as value={} [{} - {}] at 0x{:x}>".format(
            self.__class__.__name__,
            self.symbol,
            self.value,
            self.minimum,
            self.maximum,
            id(self)
        )

    @property
    def json(self):
        """
        Get a json decodable representation of this param

        :return dict: json representation
        """
        return self.__dict__

    @property
    def __dict__(self):
        return {
            'index': self.effect.params.index(self),
            'minimum': self.minimum,
            'maximum': self.maximum,
            'symbol': self.symbol,
            'value': self.value,
        }
