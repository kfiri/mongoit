"""The base class for anything that may be withing a Mongo document.
The different bson types are discribed here:
http://api.mongodb.com/python/current/api/bson/index.html
"""

import re
from bson.py3compat import text_type

SNAKE_INITIAL_RE = re.compile('_(.)')


def to_camel_case(string):
    """Converts a snake_case `string` to lowerCamelCase (Naively).
    """
    return SNAKE_INITIAL_RE.sub(lambda match: match.group(1).upper(), string)


class Field(object):
    """A generic class that represents any field from the Mongo database.
    """

    name = None
    nullable = True
    required = True
    get_default = None

    def __init__(self, name=None, nullable=None, required=None,
                 get_default=None, **kwargs):
        """Define a field in a mongodb document/sub-document.

        The livecicle of a field value is as followd:
        When quering -
          <query from mongo> -> resolve -> validate -> from_bson
        When inserting -
          to_bson -> resolve -> validate -> <insert to mongo>

        :Parameters:
          - `name` (optional): The name of the field in the Mongo database
            (this is used by :class:`ObjectField`)
          - `nullable` (optional): If ``True`` (the default), allow the value
            of this field to be ``None``. Otherwise, raise :class:`TypeError`
            (unless `default` is specified).
          - `required` (optional): If ``True`` (the default), raise
            :class:`TypeError` if this field does not exist in the query result
            that should include it (unless `default` is specified).
          - `default` (optional): Used only if `required` is ``True`` or
            if `nullable` is ``False``. When querying, use this BSON value if
            it does not exist in the query result. When updating or creating a
            new document, use this if the BSON value is not set.
          - `get_default` (optional): A getter function that can be used
            instead of `default`.
        """
        super(Field, self).__init__()

        if name is not None:
            self.required = name
        if nullable is not None:
            self.nullable = nullable
        if required is not None:
            self.required = required

        if get_default is not None:
            if 'default' in kwargs:
                raise TypeError("cannot use keyword argument 'get_default' "
                                "with the keyword argument 'default'")
            self.get_default = get_default
        elif 'default' in kwargs:
            default_bson = kwargs.pop('default')
            self.get_default = lambda: default_bson

        if kwargs:
            raise TypeError("Field() got an unexpected keyword argument(s) "
                            "%s" % ' '.join("'%s'" % arg for arg in kwargs))

    def __repr__(self):
        return type(self).__name__

    def to_bson(self, value):
        """Conferts `value` to a BSON type value.
        """
        return value

    def from_bson(self, value):
        """Conferts a BSON type `value` to a python object.
        """
        return value

    def resolve(self, value):
        """Resolve the BSON `value` by setting the default BSON value if
        `value` is ``None`` and not nullable.

        This method should never raise an exception.
        """
        if value is None and not self.nullable and self.get_default:
            return self.get_default()
        return value

    def validate(self, value):
        """Validate that the BSON `value` is valid for this field.

        :Returns:
          ``True`` if further validations are not required.
        """
        # TODO until V0.2.0: validate that the value is indeed a BSON value
        if value is None:
            if self.nullable:
                return True
            raise TypeError("value of %s may not be null because that field "
                            "is not nullable" % self)

    def get_field(self, key):
        """Get the field in the `key` position of this field.
        """
        return self.anonymous

    def _get_field_name(self, key, field):
        """Get the name of the `field` in the `key` position of this field as it
        should appear in the database.
        """
        if field.name:
            return field.name
        key = text_type(key)
        return key if key.startswith(u'_') else to_camel_case(key)

    def get_field_name(self, key):
        """Get the name of the field in the `key` position of this field as it
        should appear in the database.
        """
        return self._get_field_name(key, self.get_field(key))


class AnonymousField(Field):
    def __new__(self):
        return Field.anonymous


Field.anonymous = Field.__new__(AnonymousField)
Field.anonymous.__init__(nullable=True, required=False)
