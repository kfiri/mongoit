"""An object(/sub document) within a Mongo document."""

from bson import SON
from bson.py3compat import iteritems

from .field import Field


class Object(Field):
    """Represents an object field (sub-document) in the mongo database.
    """

    # TODO until V0.3.0: support ordering fields.
    strict = False

    def __init__(self, fields=None, strict=None, name=None, nullable=None,
                 required=None, get_default=None, **kwargs):
        """Defines an object of fields in MongoDB.

        :Parameters:
          - `fields` (optional): A mapping of a key to fields.
          - `strict` (optional): If ``True``, raise :class:`TypeError` if this
            field contains any fields that are not in the `fields` argument.
          - `**kwargs` (optional): See the documentation about
            :class:`~mongomodals.field.Field` for the full details.
        """
        super(Object, self).__init__(name=name, nullable=nullable,
                                     required=required,
                                     get_default=get_default, **kwargs)

        if strict is not None:
            self.strict = strict

        self.fields = SON()
        if fields is not None:
            self.fields.update(fields)

    def __repr__(self):
        repr_fields = u', '.join(("%s=%s" if field.required else "[%s=%s]") %
                                 (key, field)
                                 for key, field in iteritems(self.fields))
        if not self.strict:
            repr_fields += ', ...' if repr_fields else '...'
        return "%s<%s>" % (super(Object, self).__repr__(), repr_fields)

    def get_field(self, key):
        """Get the field in the `key` position of this field.
        """
        return self.fields.get(key, Field.ANONYMOUS)

    def resolve(self, value):
        """Resolve the BSON `value` by setting the default BSON value and
        resolving all of the fields that should be in `value`.

        :Returns:
          The resolved `value`.
        """
        value = super(Object, self).resolve(value)
        if value is not None:
            for key, field in iteritems(self.fields):
                name = self.get_field_name(key)
                if name in value:
                    value[name] = field.resolve(value[name])
                elif field.required and field.get_default_bson:
                    value[name] = field.resolve(field.get_default_bson())
        return value

    def validate(self, value):
        """Raises :class:`TypeError` if `value` is not an instance of
        :class:`dict` or if any validation of its fields fail.
        """
        if super(Object, self).validate(value):
            return True

        # Check the type of the BSON value.
        if not isinstance(value, dict):
            raise TypeError("value %r must be an instance of dict" % value)

        extra_names = set(value)
        # Validate each child field in the BSON object.
        for key, field in iteritems(self.fields):
            name = self.get_field_name(key)
            extra_names.difference_update((name,))
            if name in value:
                field.validate(value[name])
            elif field.required:
                raise TypeError("required field '%s' is missing for %r" %
                                (name, self))

        # If self is limiting the fields that it may contain,
        # make sure that BSON object does not contain any unexpected fields.
        if self.strict and extra_names:
            raise TypeError("field(s) %s are not excepted for %r" %
                            (', '.join(repr(n) for n in extra_names), self))
