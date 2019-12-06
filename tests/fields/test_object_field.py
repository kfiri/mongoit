import pytest

from mongomodels.fields import Field, ObjectField

# --- Test resolve method ---

def test_resolve_missing_property_without_default():
    properties = {'a': Field(required=True)}
    assert ObjectField(properties).resolve({}) == {}


def test_resolve_missing_property_with_default():
    properties = {'a': Field(required=True, default=1)}
    assert ObjectField(properties).resolve({}) == {'a': 1}


def test_resolve_property_without_default():
    properties = {'a': Field(nullable=False)}
    assert ObjectField(properties).resolve({'a': None}) == {'a': None}


def test_resolve_property_without_default():
    properties = {'a': Field(nullable=False, default=1)}
    assert ObjectField(properties).resolve({'a': None}) == {'a': 1}

# --- Test validate method ---

@pytest.mark.parametrize('value', [{}, {'a': 1}])
def test_validate_object(value):
    ObjectField(nullable=False).validate(value)


@pytest.mark.parametrize('value', [False, True, 0, 1, [1], '1', None])
def test_fails_validate_object(value):
    with pytest.raises(TypeError):
        ObjectField(nullable=False).validate(value)


@pytest.mark.parametrize('value', [{}, {'b': None}])
def test_fails_validate_object_required_property(value):
    properties = {'a': Field(required=True)}
    with pytest.raises(TypeError):
        ObjectField(properties).validate(value)


def test_fails_validate_object_property():
    properties = {'a': Field(nullable=False)}
    with pytest.raises(TypeError):
        ObjectField(properties).validate({'a': None})


def test_fails_validate_object_additional_properties():
    with pytest.raises(TypeError):
        ObjectField({}, additional_properties=False).validate({'a': None})