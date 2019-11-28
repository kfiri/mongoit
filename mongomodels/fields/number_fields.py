"""The numeric fields within a Mongo document."""

from bson import Int64
from bson.py3compat import integer_types, string_type

from .field import Field


class NumberField(Field):
    """Represents a number field in the mongo database.
    """

    def resolve(self, value):
        """Resolve the BSON `value` by converting strings and string-like types
        into numbers.
        """
        value = super(NumberField, self).resolve(value)
        if isinstance(value, (bytearray, bytes, string_type)):
            try:
                value = Int64(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass
        return value

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

    def resolve(self, value):
        """Resolve the BSON `value` by converting integer floats into
        :class:`bson.Int64`.
        """
        value = super(IntegerField, self).resolve(value)
        if isinstance(value, float) and value.is_integer():
            value = Int64(value)
        return value

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

    def resolve(self, value):
        """Resolve the BSON `value` by converting integers into :class:`float`.
        """
        value = super(RealNumberField, self).resolve(value)
        if isinstance(value, integer_types):
            value = float(value)
        return value

    def validate(self, value):
        """Raises :class:`TypeError` if `value` is not an instance of
        :class:`float`.
        """
        if super(RealNumberField, self).validate(value):
            return True
        if not isinstance(value, float):
            raise TypeError("value %r must be an instance of float" % value)
