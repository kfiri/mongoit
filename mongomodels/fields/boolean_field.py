"""A boolean field within a Mongo document."""

from .field import Field


class BooleanField(Field):
    """Represents a boolean field in the mongo database.
    """

    def validate(self, value):
        """Raises :class:`TypeError` if `value` is not an instance of bool.
        """
        if super(BooleanField, self).validate(value):
            return True
        if not isinstance(value, bool):
            raise TypeError("value %s must be an instance of bool" % value)
