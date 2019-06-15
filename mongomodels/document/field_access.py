"""
"""


class FieldAccess(object):
    """An access for a :class:`mongomodals.fields.Field`
    """

    def __init__(self, key, name, field, path=()):
        """
        """
        self.__key = key
        self.__name = name
        self.__field = field
        self.__path = path + (self,)

    def __repr__(self):
        return "<Access '%s' to %s>" % (self.get_path_as_name(), self.__field)

    def __getattr__(self, name):
        return self[name]

    def __getitem__(self, key):
        sub_field = self.__field.get_field(key)
        name = self.__field.get_field_name(key)
        return FieldAccess(key, name, sub_field, self.__path)

    def __pos__(self):
        """Get the object that represent an existing field in a Mongo query.
        """
        return self.get_operation_for(+self.__field)

    def __neg__(self):
        """Get the object that represent a non-existing field in a Mongo query.
        """
        return self.get_operation_for(-self.__field)

    def __eq__(self, value):
        """Get the object that represent the == operation in a Mongo query.
        """
        return self.get_operation_for(self.__field == value)

    def __ne__(self, value):
        """Get the object that represent the != operation in a Mongo query.
        """
        return self.get_operation_for(self.__field != value)

    def __gt__(self, value):
        """Get the object that represent the > operation in a Mongo query.
        """
        return self.get_operation_for(self.__field > value)

    def __ge__(self, value):
        """Get the object that represent the >= operation in a Mongo query.
        """
        return self.get_operation_for(self.__field >= value)

    def __lt__(self, value):
        """Get the object that represent the < operation in a Mongo query.
        """
        return self.get_operation_for(self.__field < value)

    def __le__(self, value):
        """Get the object that represent the <= operation in a Mongo query.
        """
        return self.get_operation_for(self.__field <= value)

    def get_operation_for(self, operation):
        """Get the object that represent the `operation` for the field in the
        field-access in a Mongo query.
        """
        for access in reversed(self.__path):
            operation = {access.__name: operation}
        return operation

    def get_field(self):
        return self.__field

    def get_path(self):
        return self.__path

    def get_path_as_name(self):
        return '.'.join(node.__name for node in self.__path)
