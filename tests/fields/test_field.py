import pytest

from mongomodels.fields import Field


def test_resolve_none_without_default():
    field = Field(nullable=False)
    assert field.resolve(None) is None


def test_resolve_none_with_default():
    field = Field(nullable=False, default=1)
    assert field.resolve(None) == 1


def test_validate_none_nullable():
    field = Field()
    field.validate(None)


def test_validate_none():
    field = Field(nullable=False)
    with pytest.raises(TypeError):
        field.validate(None)


def test_exists():
    assert +Field() == {'$exists': True}


def test_not_exists():
    assert -Field() == {'$exists': False}


def test_eq():
    assert (Field() == 1) == 1


def test_ne():
    assert (Field() != 1) == {'$ne': 1}


def test_gt():
    assert (Field() > 1) == {'$gt': 1}


def test_gte():
    assert (Field() >= 1) == {'$gte': 1}


def test_lt():
    assert (Field() < 1) == {'$lt': 1}


def test_lte():
    assert (Field() <= 1) == {'$lte': 1}
