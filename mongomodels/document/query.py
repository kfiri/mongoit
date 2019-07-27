"""
"""


class Query(object):
    """
    """

    def __or__(self, other):
        if not isinstance(other, Query):
            return NotImplemented
        return Query.any_of(self, other)

    def __and__(self, other):
        if not isinstance(other, Query):
            return NotImplemented
        return Query.all_of(self, other)

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


class QueryLogicalOperatorsBase(Query):
    """

    """


class QueryNot(QueryLogicalOperatorsBase):
    def __init__(self, query):
        super(QueryNot, self).__init__()
        self.query = query

    def as_query(self):
        if isinstance(self.query, QueryNot):
            return self.query.query.as_query()
        if isinstance(self.query, QueryAnyOfBase):
            return (-self.query).as_query()
        return


class QueryAnyOfBase(QueryLogicalOperatorsBase):
    """

    """
    OPERATOR = None

    def __init__(self, queries):
        """

        :param queries:
        """
        # TODO until v0.0.5: validate arguments types.
        self.queries = list(queries)

    def as_query(self):
        # TODO until v0.1.0: resolve sub-QueryAnyOf.
        return {self.OPERATOR: [query.as_query() for query in self.queries]}


class QueryAnyOf(QueryAnyOfBase):
    """

    """
    OPERATOR = '$or'

    def __neg__(self):
        return QueryNotAnyOf(self.queries)


class QueryNotAnyOf(QueryAnyOfBase):
    """

    """
    OPERATOR = '$nor'

    def __neg__(self):
        return QueryAnyOf(self.queries)


class QueryAllOf(QueryLogicalOperatorsBase):
    """

    """
    OPERATOR = '$and'

    def __init__(self, queries):
        """

        :param queries:
        """
        # TODO until v0.0.5: validate arguments types.
        self.queries = list(queries)

    def as_query(self):
        # TODO until v0.1.0: resolve sub-QueryAnyOf.
        return {self.OPERATOR: [query.as_query() for query in self.queries]}

    def __neg__(self):
        return QueryNotAnyOf(self.queries)


class QueryNotAllOf(QueryLogicalOperatorsBase):
    """

    """

    def __init__(self, queries):
        """

        :param queries:
        """
        # TODO until v0.0.5: validate arguments types.
        self.queries = list(queries)

    def as_query(self):
        # TODO until v0.1.0: resolve sub-QueryAnyOf.
        return {'$not': {QueryAllOf.OPERATOR: [query.as_query() for query in self.queries]}}

    def __neg__(self):
        return QueryAllOf(self.queries)
