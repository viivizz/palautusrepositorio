
from matchers import All, And, Or, PlaysIn, HasAtLeast, HasFewerThan


class QueryBuilder:
    def __init__(self, matchers=None):
        self._matchers = matchers if matchers is not None else []

    def plays_in(self, team):
        return QueryBuilder(self._matchers + [PlaysIn(team)])

    def has_at_least(self, value, attr):
        return QueryBuilder(self._matchers + [HasAtLeast(value, attr)])

    def has_fewer_than(self, value, attr):
        return QueryBuilder(self._matchers + [HasFewerThan(value, attr)])

    def one_of(self, *matchers):
        matchers = [matcher.build() for matcher in matchers]
        return QueryBuilder(self._matchers + [Or(*matchers)])

    def build(self):
        if not self._matchers:
            return All()

        return And(*self._matchers)
