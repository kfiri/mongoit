import pytest

from mongomodels.document.field_access import FieldAccess
from mongomodels.fields import Field, Array, Object

FIRST_FIELD = 'a'
SECOND_FIELD = 'b'


def test_access_field():
    field = Field()
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, field)
    assert field_access.get_field() is field
    assert field_access.get_path_as_name() == FIRST_FIELD


def test_access_anonymous_field():
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, Field())
    assert field_access.b.get_field() is Field.ANONYMOUS
    assert field_access.get_path_as_name() == FIRST_FIELD
    assert field_access.b.get_path_as_name() == '.'.join((FIRST_FIELD, SECOND_FIELD))


def test_access_array_field():
    array_field = Array(Field())
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, array_field)[0]
    assert field_access.get_field() is array_field.field
    assert field_access.get_path_as_name() == '.'.join((FIRST_FIELD, '0'))


def test_access_object_field():
    object_field = Object({SECOND_FIELD: Field()})
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, object_field).b
    assert field_access.get_field() is object_field.fields[SECOND_FIELD]
    assert field_access.get_path_as_name() == '.'.join((FIRST_FIELD, SECOND_FIELD))


def test_access_object_array_field():
    object_field = Object({SECOND_FIELD: Field()})
    array_field = Array(object_field)
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, array_field).b
    assert field_access.get_field() is object_field.fields[SECOND_FIELD]
    assert field_access.get_path_as_name() == '.'.join((FIRST_FIELD, SECOND_FIELD))
