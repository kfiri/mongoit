"""A datetime field within a Mongo document."""
import pytz
from datetime import datetime

from .field import Field

NOW = 'now'


class DatetimeField(Field):
    """Represents a boolean field in the mongo database.
    """
    tzinfo = pytz.utc

    def __init__(self, tzinfo=None, name=None, nullable=None, required=None,
                 get_default=None, **kwargs):
        """Defines an array of a field in MongoDB.

        The datetime field always saves the datetime as UTC in the database for
        2 main reasons:
          - MongoDB saves only naive datetime objects.
          - You can compare datetimes in the database with one another only
            when they are in the same timezone.
        
        In order to get the current datetime as default use the argument
        get_default='now'.

        :Parameters:
          - `field`: The field of the items in the array. The `name` and
            the `required` attributes of the `field` are discarded.
          - `get_default_now`: Can me 
          - `**kwargs` (optional): See the documentation about
            :class:`~mongomodals.field.Field` for the full details.
        """
        if tzinfo:
            self.tzinfo = tzinfo
        if get_default == NOW:
            get_default = lambda: datetime.now(tz=self.tzinfo)
        super(DatetimeField, self).__init__(name=name, nullable=nullable,
                                            required=required,
                                            get_default=get_default, **kwargs)

    def to_bson(self, value):
        """Convert a timezone aware datetime to a naive datetime object in UTC.
        """
        # TODO until V0.5.0: pymongo implements a handler for tz aware
        # datetimes. Should we still implement this?
        return pytz.utc.normalize(value).replace(tzinfo=None)

    def from_bson(self, value):
        """Convert a naive datetime object in UTC to a datetime in the timezone
        of the field.
        """
        return self.tzinfo.fromutc(value)
    
    def resolve(self, value):
        """Resolve the BSON `value` localizing it to the field's timezone if it
        is a naive datetime.

        :Returns:
          The resolved `value`.
        """
        value = super(DatetimeField, self).resolve(value)
        if isinstance(value, datetime) and not value.tzinfo:
            try:
                value = self.tzinfo.localize(value, is_dst=None)
            except pytz.AmbiguousTimeError:
                pass
        return value

    def validate(self, value):
        """Raises :class:`TypeError` if `value` is not an instance of datetime
        or if it is a naive datetime.
        """
        if super(DatetimeField, self).validate(value):
            return True
        if not isinstance(value, datetime):
            raise TypeError("value %s must be an instance of datetime" % value)
        # TODO: we should not check this for data from the database.
        elif not value.tzinfo:
            raise TypeError("value %s is naive" % value)
