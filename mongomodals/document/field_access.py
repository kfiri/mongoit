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

    def get_field(self):
        return self.__field

    def get_path(self):
        return self.__path

    def get_path_as_name(self):
        return '.'.join(node.__name for node in self.__path)
