"""An object(/sub document) within a Mongo document."""

from bson import SON
from bson.py3compat import iteritems

from .field import Field


class ObjectField(Field):
    """Represents an object field (sub-document) in the mongo database.
    """

    # TODO until V0.3.0: support ordering properties.
    # TODO until V0.4.0: support non boolean additional_properties.
    additional_properties = True

    def __init__(self, properties=None, additional_properties=None, name=None,
                 nullable=None, required=None, get_default=None, **kwargs):
        """Defines an object of fields in MongoDB.

        :Parameters:
          - `properties` (optional): A mapping of a key to a field.
          - `additional_properties` (optional): If ``True``, raise
            :class:`TypeError` if this field contains any properties that are
            not in the object's `properties`.
          - `**kwargs` (optional): See the documentation about
            :class:`~mongomodals.field.Field` for the full details.
        """
        super(ObjectField, self).__init__(name=name, nullable=nullable,
                                          required=required,
                                          get_default=get_default, **kwargs)

        if additional_properties is not None:
            self.additional_properties = additional_properties

        self.properties = SON()
        if properties is not None:
            self.properties.update(properties)

    def __repr__(self):
        repr_fields = u', '.join(("%s=%s" if prop.required else "[%s=%s]") %
                                 (key, prop)
                                 for key, prop in iteritems(self.properties))
        if self.additional_properties:
            repr_fields += ', ...' if repr_fields else '...'
        return "%s<%s>" % (super(ObjectField, self).__repr__(), repr_fields)

    def get_field(self, key):
        """Get the property in the `key` position of this field.
        """
        return self.properties.get(key, Field.ANONYMOUS)

    def resolve(self, value):
        """Resolve the BSON `value` by setting the default BSON value and
        resolving all of the fields that should be in `value`.

        :Returns:
          The resolved `value`.
        """
        value = super(ObjectField, self).resolve(value)
        if value is not None:
            for key, prop in iteritems(self.properties):
                name = self.get_field_name(key)
                if name in value:
                    value[name] = prop.resolve(value[name])
                elif prop.required and prop.get_default:
                    value[name] = prop.resolve(prop.get_default())
        return value

    def validate(self, value):
        """Raises :class:`TypeError` if `value` is not an instance of
        :class:`dict` or if any validation of its fields fail.
        """
        if super(ObjectField, self).validate(value):
            return True

        # Check the type of the BSON value.
        if not isinstance(value, dict):
            raise TypeError("value %r must be an instance of dict" % value)

        extra_names = set(value)
        # Validate each child prop in the object.
        for key, prop in iteritems(self.properties):
            name = self.get_field_name(key)
            extra_names.difference_update((name,))
            if name in value:
                prop.validate(value[name])
            elif prop.required:
                raise TypeError("required property '%s' is missing for %r" %
                                (name, self))

        # If self is limiting the fields that it may contain,
        # make sure that object does not contain any unexpected fields.
        if not self.additional_properties and extra_names:
            raise TypeError("properties %s are not excepted for %r" %
                            (', '.join(repr(n) for n in extra_names), self))
