"""An array within a Mongo document."""

from .field import Field


class Array(Field):
    """Represents an array field in the mongo database.
    """

    def __init__(self, field, name=None, nullable=None, required=None,
                 get_default=None, **kwargs):
        """Defines an array of a field in MongoDB.

        :Parameters:
          - `field`: The field of the items in the array. The `name` and
            the `required` attributes of the `field` are discarded.
          - `**kwargs` (optional): See the documentation about
            :class:`~mongomodals.field.Field`
        """
        super(Array, self).__init__(name=field.name, nullable=nullable,
                                    required=field.required,
                                    get_default=get_default, **kwargs)
        self.field = field

    def __repr__(self):
        return "%s<%r>" % (super(Array, self).__repr__(), self.field)

    def resolve(self, value):
        """Resolve the BSON `value` by setting the default BSON value and
        resolving all of the items in the `value`.

        :Returns:
          The resolved `value`.
        """
        value = super(Array, self).resolve(value)
        if value is not None:
            for i, item in enumerate(value):
                value[i] = self.field.resolve(item)
        return value

    def validate(self, value):
        """Raises :class:`TypeError` if `value` is not an instance of
        :class:`list` or if any validation of the items fail.
        """
        if super(Array, self).validate(value):
            return True
        if not isinstance(value, list):
            raise TypeError("value %s must be an instance of list" % value)
        # TODO until V0.3.0: implement min_length and max_length
        # if self.min_length > len(value):
        #     raise TypeError("array value must have at least %s item(s)" %
        #                     self.min_length)
        for item in value:
            self.field.validate(item)
