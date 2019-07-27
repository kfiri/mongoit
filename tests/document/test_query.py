import pytest

from mongomodels.document.query import QueryRaw, QueryNot, QueryAnyOf, QueryNotAnyOf, QueryAllOf, QueryNotAllOf


@pytest.fixture
def q():
    return {'a': 1}


@pytest.fixture
def raw_query(q):
    return QueryRaw(q)


@pytest.fixture
def raw_query2(q):
    return QueryRaw({'b': 2})


def test_raw_query(raw_query, q):
    assert raw_query.as_query() == q


class TestLogicalOperators(object):
    def test_not_query(self, raw_query):
        assert QueryNot(raw_query).as_query() == {'$not': raw_query.as_query()}

    def test_not_query_magic(self, raw_query):
        assert (-raw_query).as_query() == QueryNot(raw_query).as_query()

    def test_not_not_query(self, raw_query):
        query = QueryNot(QueryNot(raw_query))
        assert query.as_query() == raw_query.as_query()

    @pytest.mark.parametrize(('operation_type', 'not_operation_type'), [
        (QueryAnyOf, QueryNotAnyOf),
        (QueryNotAnyOf, QueryAnyOf),
        (QueryAllOf, QueryNotAllOf),
        (QueryNotAllOf, QueryAllOf)
    ])
    def test_not_logical_operation(self, raw_query, operation_type, not_operation_type):
        query = QueryNot(operation_type([raw_query]))
        assert query.as_query() == not_operation_type([raw_query]).as_query()

    def test_any_of_query(self, raw_query, raw_query2):
        assert QueryAnyOf([raw_query, raw_query2]).as_query() == {'$or': [raw_query.as_query(), raw_query2.as_query()]}

    def test_any_of_query_magic(self, raw_query, raw_query2):
        assert (raw_query | raw_query2).as_query() == QueryAnyOf([raw_query, raw_query2]).as_query()

    def test_not_any_of_query(self, raw_query, raw_query2):
        assert QueryNotAnyOf([raw_query, raw_query2]).as_query() == {
            '$nor': [raw_query.as_query(), raw_query2.as_query()]}

    def test_not_any_of_query_magic(self, raw_query, raw_query2):
        assert (-(raw_query | raw_query2)).as_query() == QueryNotAnyOf([raw_query, raw_query2]).as_query()

    def test_all_of_query(self, raw_query, raw_query2):
        assert QueryAllOf([raw_query, raw_query2]).as_query() == {'$and': [raw_query.as_query(), raw_query2.as_query()]}

    def test_all_of_query_magic(self, raw_query, raw_query2):
        assert (raw_query & raw_query2).as_query() == QueryAllOf([raw_query, raw_query2]).as_query()

    def test_not_all_of_query(self, raw_query, raw_query2):
        assert QueryNotAllOf([raw_query, raw_query2]).as_query() == {
            '$not': {'$and': [raw_query.as_query(), raw_query2.as_query()]}}

    def test_not_all_of_query_magic(self, raw_query, raw_query2):
        assert (-(raw_query & raw_query2)).as_query() == QueryNotAllOf([raw_query, raw_query2]).as_query()
