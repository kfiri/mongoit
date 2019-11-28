"""
"""


class Query(object):
    """
    """

    def __add__(self, other):
        return self & other

    def __sub__(self, other):
        return self & QueryNot(other)

    def __or__(self, other):
        if not isinstance(other, Query):
            return NotImplemented
        return Query.any_of(self, other)

    def __and__(self, other):
        if not isinstance(other, Query):
            return NotImplemented
        return Query.all_of(self, other)

    def __xor__(self, other):
        if not isinstance(other, Query):
            return NotImplemented
        return Query.one_of(self, other)

    def __neg__(self):
        return QueryNot(self)

    def as_query(self):
        """
        Get the query as it should be sent to pymongo.
        """
        raise NotImplementedError

    @classmethod
    def any_of(cls, *queries):
        """
        """
        return QueryAnyOf(queries)

    @classmethod
    def all_of(cls, *queries):
        """
        """
        return QueryAllOf(queries)

    @classmethod
    def one_of(cls, *queries):
        """
        """
        raise TypeError('one-of queries are not supported')


class QueryRaw(Query):
    """

    """

    def __init__(self, query):
        """

        :param query:
        """
        super(QueryRaw, self).__init__()
        self.raw_query = query

    def as_query(self):
        return self.raw_query


class LogicalOperator(Query):
    """

    """


class QueryNot(LogicalOperator):
    def __init__(self, query):
        super(QueryNot, self).__init__()
        self.query = query

    def __neg__(self):
        return self.query

    def as_query(self):
        # TODO until v0.0.5: validate query type.
        if isinstance(self.query, QueryNot):
            return self.query.query.as_query()
        if isinstance(self.query, QueriesLogicalOperator):
            return (-self.query).as_query()
        return {'$not': self.query.as_query()}


class QueriesLogicalOperator(LogicalOperator):
    """

    """
    OPERATOR = None

    def __init__(self, queries):
        """

        :param queries:
        """
        super(QueriesLogicalOperator, self).__init__()
        self.queries = tuple(queries)

    def as_query(self):
        # TODO until v0.0.5: validate queries types.
        # TODO until v0.4.0: resolve sub-QueryAnyOf/QueryAllOf.
        # TODO until v0.4.0: convert a query with only 'not' sub-queries
        # (and(not a, not b) -> nor(a, b)).
        return {self.OPERATOR: [query.as_query() for query in self.queries]}


class QueryAnyOf(QueriesLogicalOperator):
    """

    """
    OPERATOR = '$or'

    def __neg__(self):
        return QueryNotAnyOf(self.queries)


class QueryNotAnyOf(QueriesLogicalOperator):
    """

    """
    OPERATOR = '$nor'

    def __neg__(self):
        return QueryAnyOf(self.queries)


class QueryAllOf(QueriesLogicalOperator):
    """

    """
    OPERATOR = '$and'

    def __neg__(self):
        return QueryNotAllOf(self.queries)


class QueryNotAllOf(QueriesLogicalOperator):
    """

    """

    def __neg__(self):
        return QueryAllOf(self.queries)

    def as_query(self):
        return {'$not': QueryAllOf(self.queries).as_query()}

