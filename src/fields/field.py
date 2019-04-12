
class Field(object):
    """A generic class that represents any field from the mongo database.
    """

    def __init__(self, nullable=True, **kwargs):
        """Represent a field in a mongodb document/sub-document.

        :Parameters:
          - `nullable` (optional): If ``True`` (the default), allow the value
            of this field to be ``None``. Otherwise, raise :class:`TypeError`
            (unless `default_bson` is specified).
          - `strict` (optional): If ``True`` (the default is ``True`` if
            `nullable` is ``False`` otherwise ``True``), raise
            :class:`TypeError` if this field does not exist in the query result
            that should include it (unless `default_bson` is specified).
          - `default_bson`(optional): Used only if `strict` is ``True`` or
            if `nullable` is ``False``. When querying, use this BSON value if
            it does not exist in the query result. When updating or creating a
            new document, use this if the value was not specified explicitly.
        """
        super(Field, self).__init__()
        self.nullable = kwargs.pop('nullable', True)
        self.strict = kwargs.pop('strict', not self.nullable)
        self._usedefault = 'default_bson' in kwargs
        self.default_bson = kwargs.pop('default_bson', None)
        if kwargs:
            raise TypeError("Field() got an unexpected keyword argument(s) "
                            "%s" % ' '.join("'%s'" % arg for arg in kwargs))

    def __repr__(self):
        return type(self).__name__

    def to_bson(self, value):
        """Conferts `value` to a BSON type value.
        """
        self.validate_bson(value)
        if value is None and not self.nullable and self._usedefault:
            return self.default_bson
        return value

    def from_bson(self, value):
        """Conferts a BSON type `value` to a python object.
        """
        self.validate_bson(value)
        if value is None and not self.nullable and self._usedefault:
            return self.default_bson
        return value

    def validate_bson(self, value):
        """Validate that the BSON `value` is valid for this field.

        :Returns:
          ``True`` if further validations are not required.
        """
        if value is None:
            if self.nullable or self._usedefault:
                return True
            raise TypeError("value of %s may not be null because " % self +
                            "that field is not nullable")
