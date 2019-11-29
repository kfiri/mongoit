import pytest

from mongomodels.fields import BooleanField


@pytest.mark.parametrize('value', [True, False])
def test_validate_number(value):
    BooleanField(nullable=False).validate(value)


@pytest.mark.parametrize('value', ['', 0, 1, [], {}, None])
def test_fails_validate_number(value):
    with pytest.raises(TypeError):
        BooleanField(nullable=False).validate(value)
