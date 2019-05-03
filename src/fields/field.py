"""The base class for anything that may be withing a Mongo document."""


class Field(object):
    """A generic class that represents any field from the Mongo database.
    """

    nullable = True
    required = True

    def __init__(self, **kwargs):
        """Represent a field in a mongodb document/sub-document.

        The livecicle of a field value is as followd:
        When quering -
          <query from mongo> -> resolve_bson -> validate_bson -> from_bson -> resolve_value -> validate_value
        When inserting -
          resolve_value -> validate_value -> to_bson -> resolve_bson -> validate_bson -> <insert to mongo>

        :Parameters:
          - `nullable` (optional): If ``True`` (the default), allow the value
            of this field to be ``None``. Otherwise, raise :class:`TypeError`
            (unless `default_bson` is specified).
          - `required` (optional): If ``True`` (the default), raise
            :class:`TypeError` if this field does not exist in the query result
            that should include it (unless `default_bson` is specified).
          - `default_bson` (optional): Used only if `required` is ``True`` or
            if `nullable` is ``False``. When querying, use this BSON value if
            it does not exist in the query result. When updating or creating a
            new document, use this if the BSON value does not exist.
          - `get_default_bson` (optional): Can be used as a getter function
            instead of `default_bson`.
          - `default_value` (optional): Used only if `required` is ``True``.
            When updating or creating a new document, use this if the value is
            not specified explicitly.
          - `get_default_value` (optional): Can be used as a getter function
            instead of `default_value`.
        """
        super(Field, self).__init__()

        if 'nullable' in kwargs:
            self.nullable = kwargs.pop('nullable')
        if 'required' in kwargs:
            self.required = kwargs.pop('required')

        # TODO until V0.0.1: implement default bson and default value.

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

    def resolve_bson(self, value):
        """Resolve the BSON `value` by setting the default BSON value if
        `value` is ``None`` and not nullable.

        :Returns:
          The resolved BSON value.
        """
        # TODO until V0.0.1: implement default bson and default value.
        # if value is None and not self.nullable and self.get_default_bson:
        #     return self.get_default_bson()
        return value

    def validate_bson(self, value):
        """Validate that the BSON `value` is valid for this field.

        :Returns:
          ``True`` if further validations are not required.
        """
        # TODO until V0.1.0: validate that the value is indeed a BSON value
        if value is None:
            if self.nullable:
                return True
            raise TypeError("value of %s may not be null because that field "
                            "is not nullable" % self)

    def resolve_value(self, value):
        """Resolve `value`.

        :Returns:
          The resolved value.
        """
        return value

    def validate_value(self, value):
        """Validate that the `value` is valid for this field.

        :Returns:
          ``True`` if further validations are not required.
        """
        pass
