import pytest

from bson import Int64

from mongomodals.fields import NumberField, IntegerField, RealNumberField


@pytest.mark.parametrize('value', [1, 0, -1, 1.1, Int64(1)])
def test_validate_number(value):
    NumberField(nullable=False).validate(value)


@pytest.mark.parametrize('value', [[], '', '1', {'a': 1}])
def test_fails_validate_number(value):
    with pytest.raises(TypeError):
        NumberField(nullable=False).validate(value)


@pytest.mark.parametrize('value', [1, 0, -1, Int64(1)])
def test_validate_integer(value):
    IntegerField(nullable=False).validate(value)


@pytest.mark.parametrize('value', [1.1, [], '', '1', {'a': 1}])
def test_fails_validate_integer(value):
    with pytest.raises(TypeError):
        IntegerField(nullable=False).validate(value)


@pytest.mark.parametrize('value', [0.0, 1.1])
def test_validate_real_number(value):
    RealNumberField(nullable=False).validate(value)


@pytest.mark.parametrize('value', [1, 0, -1, Int64(1), [], '', '1', {'a': 1}])
def test_fails_validate_real_number(value):
    with pytest.raises(TypeError):
        RealNumberField(nullable=False).validate(value)
