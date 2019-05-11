"""The numeric fields within a Mongo document."""

from bson import Int64
from bson.py3compat import integer_types

from .field import Field


class NumberField(Field):
    """Represents a number field in the mongo database.
    """

    def validate(self, value):
        """Raises :class:`TypeError` if `value` is not an instance of a number.
        """
        if super(NumberField, self).validate(value):
            return True
        if not (isinstance(value, integer_types) or isinstance(value, float)):
            raise TypeError("value %r must be an instance of a number" % value)


class IntegerField(NumberField):
    """Represents an integer field in the mongo database.
    """

    def validate(self, value):
        """Raises :class:`TypeError` if `value` is not an instance of an
        integer.
        """
        if super(IntegerField, self).validate(value):
            return True
        if not isinstance(value, integer_types):
            raise TypeError("value %r must be an instance of an integer" %
                            value)


class RealNumberField(NumberField):
    """Represents an real number (float) field in the mongo database.
    """

    def validate(self, value):
        """Raises :class:`TypeError` if `value` is not an instance of
        :class:`float`.
        """
        if super(RealNumberField, self).validate(value):
            return True
        if not isinstance(value, float):
            raise TypeError("value %r must be an instance of float" % value)
