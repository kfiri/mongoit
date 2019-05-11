"""A string field within a Mongo document."""

from bson.py3compat import string_type

from .field import Field


class StringField(Field):
    """Represents a string field in the mongo database.
    """

    def validate(self, value):
        """Raises :class:`TypeError` if `value` is not an instance of
        :class:`str` (:class:`basestring` in python 2).
        """
        if super(StringField, self).validate(value):
            return True
        if not isinstance(value, string_type):
            raise TypeError("value %s must be an instance of %s" %
                            (value, string_type.__name__))
