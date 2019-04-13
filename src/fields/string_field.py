from bson.py3compat import text_type

from .field import Field


class TextField(Field):
    """Represents a string field in the mongo database.
    """

    def validate_bson(self, value):
        """Raises :class:`TypeError` if `value` is not an instance of 
        :class:`str` (:class:`unicode` in python 2).
        """
        if super(TextField, self).validate_bson(value):
            return True
        if not isinstance(value, text_type):
            raise TypeError("value %s must be an instance of %s" %
                            (value, text_type.__name__))
