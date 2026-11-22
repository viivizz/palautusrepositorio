import re

from query_builder import QueryBuilder


NUMERIC_ATTRIBUTES = {"goals", "assists", "points"}
TEAM_QUERY = re.compile(r"^team\s*=\s*([A-Za-z0-9]+)\s*$", re.IGNORECASE)
NUMBER_QUERY = re.compile(
    r"^([A-Za-z][A-Za-z0-9_]*)\s*(>=|<)\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))\s*$"
)


def _number(value):
    if "." in value:
        return float(value)
    return int(value)


def _atomic_query(condition):
    team_match = TEAM_QUERY.fullmatch(condition)
    if team_match:
        return QueryBuilder().plays_in(team_match.group(1))

    number_match = NUMBER_QUERY.fullmatch(condition)
    if not number_match:
        raise ValueError(f"Virheellinen kyselyehto: '{condition}'")

    attribute, operator, value = number_match.groups()
    attribute = attribute.lower()
    if attribute not in NUMERIC_ATTRIBUTES:
        raise ValueError(f"Tuntematon numeerinen attribuutti: '{attribute}'")

    number = _number(value)
    if operator == ">=":
        return QueryBuilder().has_at_least(number, attribute)
    return QueryBuilder().has_fewer_than(number, attribute)


def _and_group(group):
    conditions = re.split(r"\s+and\s+", group.strip(), flags=re.IGNORECASE)
    if not conditions or any(not condition.strip() for condition in conditions):
        raise ValueError("Kyselyssa on tyhja and-ehto")

    matchers = []
    for condition in conditions:
        atomic_builder = _atomic_query(condition.strip())
        matchers.extend(atomic_builder._matchers)
    return QueryBuilder(matchers)


def parse(query):
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Kysely ei saa olla tyhja")

    or_groups = re.split(r"\s+or\s+", query.strip(), flags=re.IGNORECASE)
    if any(not group.strip() for group in or_groups):
        raise ValueError("Kyselyssa on tyhja or-ehto")

    and_builders = [_and_group(group) for group in or_groups]
    if len(and_builders) == 1:
        return and_builders[0].build()

    return QueryBuilder().one_of(*and_builders).build()
