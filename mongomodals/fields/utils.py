import re

SNAKE_INITIAL_RE = re.compile('_(.)')


def to_camel_case(string):
    """Converts a snake_case `string` to lowerCamelCase (Naively).
    """
    return SNAKE_INITIAL_RE.sub(lambda match: match.group(1).upper(), string)


def get_field_name(key, field):
    """Get the field name as it should appear in the database.
    """
    if field.name:
        return field.name
    key = str(key)
    return key if key.startswith('_') else to_camel_case(key)
