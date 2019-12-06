import pytest

from mongomodels.fields import StringField


@pytest.mark.parametrize('value', ['str', u'unicode str'])
def test_validate_str(value):
    StringField(nullable=False).validate(value)


@pytest.mark.parametrize('value', [False, True, 0, 1, [], {}, None])
def test_fails_validate_str(value):
    with pytest.raises(TypeError):
        StringField(nullable=False).validate(value)
