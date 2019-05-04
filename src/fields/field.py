"""The base class for anything that may be withing a Mongo document."""


class Field(object):
    """A generic class that represents any field from the Mongo database.
    """

    name = None
    nullable = True
    required = True
    get_default_bson = None
    get_default_value = None

    def __init__(self, **kwargs):
        """Represent a field in a mongodb document/sub-document.

        The livecicle of a field value is as followd:
        When quering -
          <query from mongo> -> resolve_bson -> validate_bson -> from_bson -> resolve_value -> validate_value
        When inserting -
          resolve_value -> validate_value -> to_bson -> resolve_bson -> validate_bson -> <insert to mongo>

        :Parameters:
          - `name` (optional): The name of the field in the Mongo database
            (this is used by :class:`ObjectField`)
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

        if 'name' in kwargs:
            self.required = kwargs.pop('name')
        if 'nullable' in kwargs:
            self.nullable = kwargs.pop('nullable')
        if 'required' in kwargs:
            self.required = kwargs.pop('required')

        get_default_bson = None
        if 'get_default_bson' in kwargs:
            get_default_bson = kwargs.pop('get_default_bson')
        if 'default_bson' in kwargs:
            if get_default_bson:
                raise TypeError("cannot use keyword argument 'default_bson' "
                                "with 'get_default_bson'")
            default_bson = kwargs.pop('default_bson')
            get_default_bson = lambda: default_bson
        if get_default_bson:
            self.get_default_bson = get_default_bson

        get_default_value = None
        if 'get_default_value' in kwargs:
            get_default_value = kwargs.pop('get_default_value')
        if 'default_value' in kwargs:
            if get_default_value:
                raise TypeError("cannot use keyword argument 'default_value' "
                                "with 'get_default_value'")
            default_value = kwargs.pop('default_value')
            get_default_value = lambda: default_value
        if get_default_value:
            self.get_default_value = get_default_value

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
        if value is None and not self.nullable and self.get_default_bson:
            return self.get_default_bson()
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
        """Resolve `value` by setting the default value if `value` is ``None``
        and not nullable.

        :Returns:
          The resolved value.
        """
        if value is None and not self.nullable and self.get_default_value:
            return self.get_default_value()
        return value

    def validate_value(self, value):
        """Validate that the `value` is valid for this field.

        :Returns:
          ``True`` if further validations are not required.
        """
        pass
