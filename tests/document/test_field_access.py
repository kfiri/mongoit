import pytest

from mongomodels.document.field_access import FieldAccess
from mongomodels.fields import Field, ArrayField, ObjectField

FIRST_NAME = 'a'
SECOND_NAME = 'b'


@pytest.fixture()
def field():
    return Field()

@pytest.fixture()
def field_access(field):
    return FieldAccess(FIRST_NAME, FIRST_NAME, field, path=())


def test_access_field(field, field_access):
    assert field_access.get_field() is field
    assert field_access.get_path_as_name() == FIRST_NAME


def test_access_anonymous_field(field_access):
    assert field_access.b.get_field() is Field.ANONYMOUS
    assert field_access.get_path_as_name() == FIRST_NAME
    assert (field_access.b.get_path_as_name() ==
            '.'.join((FIRST_NAME, SECOND_NAME)))


def test_access_array_field():
    array_field = ArrayField(Field())
    field_access = FieldAccess(FIRST_NAME, FIRST_NAME, array_field)[0]
    assert field_access.get_field() is array_field.items
    assert field_access.get_path_as_name() == '.'.join((FIRST_NAME, '0'))


def test_access_object_field():
    object_field = ObjectField({SECOND_NAME: Field()})
    field_access = FieldAccess(FIRST_NAME, FIRST_NAME, object_field, ()).b
    assert field_access.get_field() is object_field.properties[SECOND_NAME]
    assert (field_access.get_path_as_name() ==
            '.'.join((FIRST_NAME, SECOND_NAME)))


def test_access_object_array_field(field):
    object_field = ObjectField({SECOND_NAME: field})
    array_field = ArrayField(object_field)
    field_access = FieldAccess(FIRST_NAME, FIRST_NAME, array_field, ()).b
    assert field_access.get_field() is object_field.properties[SECOND_NAME]
    assert (field_access.get_path_as_name() ==
            '.'.join((FIRST_NAME, SECOND_NAME)))


def test_field_access_exists(field_access):
    assert +field_access == {FIRST_NAME: {'$exists': True}}


def test_field_access_not_exists(field_access):
    assert -field_access == {FIRST_NAME: {'$exists': False}}


def test_field_access_eq(field_access):
    assert (field_access == 1) == {FIRST_NAME: 1}


def test_field_access_ne(field_access):
    assert (field_access != 1) == {FIRST_NAME: {'$ne': 1}}


def test_field_access_gt(field_access):
    assert (field_access > 1) == {FIRST_NAME: {'$gt': 1}}


def test_field_access_gte(field_access):
    assert (field_access >= 1) == {FIRST_NAME: {'$gte': 1}}


def test_field_access_lt(field_access):
    assert (field_access < 1) == {FIRST_NAME: {'$lt': 1}}


def test_field_access_lte(field_access):
    assert (field_access <= 1) == {FIRST_NAME: {'$lte': 1}}


def test_nested_field_access_eq(field_access):
    assert ((field_access[SECOND_NAME] == 1) ==
            {FIRST_NAME: {SECOND_NAME: 1}})


def test_nested_field_access_ne(field_access):
    assert ((field_access[SECOND_NAME] != 1) ==
            {FIRST_NAME: {SECOND_NAME: {'$ne': 1}}})
