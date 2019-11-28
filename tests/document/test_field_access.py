from mongomodels.document.field_access import FieldAccess
from mongomodels.fields import Field, ArrayField, ObjectField

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
    assert (field_access.b.get_path_as_name() ==
            '.'.join((FIRST_FIELD, SECOND_FIELD)))


def test_access_array_field():
    array_field = ArrayField(Field())
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, array_field)[0]
    assert field_access.get_field() is array_field.field
    assert field_access.get_path_as_name() == '.'.join((FIRST_FIELD, '0'))


def test_access_ObjectField_field():
    ObjectField_field = ObjectField({SECOND_FIELD: Field()})
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, ObjectField_field).b
    assert field_access.get_field() is ObjectField_field.properties[SECOND_FIELD]
    assert (field_access.get_path_as_name() ==
            '.'.join((FIRST_FIELD, SECOND_FIELD)))


def test_access_ObjectField_array_field():
    ObjectField_field = ObjectField({SECOND_FIELD: Field()})
    array_field = ArrayField(ObjectField_field)
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, array_field).b
    assert field_access.get_field() is ObjectField_field.properties[SECOND_FIELD]
    assert (field_access.get_path_as_name() ==
            '.'.join((FIRST_FIELD, SECOND_FIELD)))


def test_field_access_exists():
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, Field())
    assert +field_access == {FIRST_FIELD: {'$exists': True}}


def test_field_access_not_exists():
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, Field())
    assert -field_access == {FIRST_FIELD: {'$exists': False}}


def test_field_access_eq():
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, Field())
    assert (field_access == 1) == {FIRST_FIELD: 1}


def test_field_access_ne():
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, Field())
    assert (field_access != 1) == {FIRST_FIELD: {'$ne': 1}}


def test_field_access_gt():
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, Field())
    assert (field_access > 1) == {FIRST_FIELD: {'$gt': 1}}


def test_field_access_gte():
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, Field())
    assert (field_access >= 1) == {FIRST_FIELD: {'$gte': 1}}


def test_field_access_lt():
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, Field())
    assert (field_access < 1) == {FIRST_FIELD: {'$lt': 1}}


def test_field_access_lte():
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, Field())
    assert (field_access <= 1) == {FIRST_FIELD: {'$lte': 1}}


def test_nested_field_access_eq():
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, Field())
    assert ((field_access[SECOND_FIELD] == 1) ==
            {FIRST_FIELD: {SECOND_FIELD: 1}})


def test_nested_field_access_ne():
    field_access = FieldAccess(FIRST_FIELD, FIRST_FIELD, Field())
    assert ((field_access[SECOND_FIELD] != 1) ==
            {FIRST_FIELD: {SECOND_FIELD: {'$ne': 1}}})
