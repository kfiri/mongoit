"""An array within a Mongo document."""

from bson.py3compat import integer_types

from .field import Field


class ArrayField(Field):
    """Represents an array field in the mongo database.
    """

    def __init__(self, items, name=None, nullable=None, required=None,
                 get_default=None, **kwargs):
        """Defines an array of a field in MongoDB.

        :Parameters:
          - `items`: The field of the items in the array. The `name` and
            the `required` attributes of the `items` are discarded.
          - `**kwargs` (optional): See the documentation about
            :class:`~mongomodals.field.Field` for the full details.
        """
        super(ArrayField, self).__init__(name=name, nullable=nullable,
                                    required=required,
                                    get_default=get_default, **kwargs)
        self.items = items

    def __repr__(self):
        return "%s<%r>" % (super(ArrayField, self).__repr__(), self.items)

    def get_field(self, key):
        """Get the field in the `key` position of this field.
        """
        if isinstance(key, integer_types):
            return self.items
        return self.items.get_field(key)

    def resolve(self, value):
        """Resolve the BSON `value` by setting the default BSON value and
        resolving all of the items in the `value`.

        :Returns:
          The resolved `value`.
        """
        value = super(ArrayField, self).resolve(value)
        if value is not None:
            for i, item in enumerate(value):
                value[i] = self.items.resolve(item)
        return value

    def validate(self, value):
        """Raises :class:`TypeError` if `value` is not an instance of
        :class:`list` or if any validation of its items fail.
        """
        if super(ArrayField, self).validate(value):
            return True
        if not isinstance(value, list):
            raise TypeError("value %s must be an instance of list" % value)
        # TODO until V0.3.0: implement min_length and max_length
        # if self.min_length > len(value):
        #     raise TypeError("array value must have at least %s item(s)" %
        #                     self.min_length)
        for item in value:
            self.items.validate(item)
