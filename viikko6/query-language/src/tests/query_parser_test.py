import unittest

from player import Player
from query_parser import parse
from statistics import Statistics


class FakeReader:
    def __init__(self, players):
        self._players = players

    def get_players(self):
        return self._players


class TestQueryParser(unittest.TestCase):
    def setUp(self):
        self.nyr_low = Player("A", "NYR", 9, 5)
        self.nyr_medium = Player("B", "NYR", 10, 19)
        self.nyr_high = Player("C", "NYR", 20, 20)
        self.edm = Player("D", "EDM", 15, 12)
        self.edm_low = Player("E", "EDM", 5, 8)
        self.players = [
            self.nyr_low,
            self.nyr_medium,
            self.nyr_high,
            self.edm,
            self.edm_low,
        ]

    def test_team_condition(self):
        matcher = parse("team = NYR")

        matches = [player for player in self.players if matcher.test(player)]

        self.assertEqual(matches, [self.nyr_low, self.nyr_medium, self.nyr_high])

    def test_at_least_boundary_is_inclusive(self):
        matcher = parse("goals >= 10")

        matches = [player for player in self.players if matcher.test(player)]

        self.assertIn(self.nyr_medium, matches)
        self.assertNotIn(self.nyr_low, matches)

    def test_fewer_than_boundary_is_exclusive(self):
        matcher = parse("assists < 20")

        matches = [player for player in self.players if matcher.test(player)]

        self.assertIn(self.nyr_medium, matches)
        self.assertNotIn(self.nyr_high, matches)

    def test_and_requires_all_conditions(self):
        matcher = parse("team = NYR and goals >= 10")

        matches = [player for player in self.players if matcher.test(player)]

        self.assertEqual(matches, [self.nyr_medium, self.nyr_high])

    def test_and_bounds_form_closed_open_range(self):
        matcher = parse("goals >= 10 and goals < 20")

        matches = [player for player in self.players if matcher.test(player)]

        self.assertEqual(matches, [self.nyr_medium, self.edm])

    def test_and_binds_more_strongly_than_or(self):
        matcher = parse("team = NYR or team = EDM and goals >= 15")

        matches = [player for player in self.players if matcher.test(player)]

        self.assertEqual(matches, [self.nyr_low, self.nyr_medium, self.nyr_high, self.edm])

    def test_multiple_or_conditions(self):
        matcher = parse("team = NYR or team = EDM")

        matches = [player for player in self.players if matcher.test(player)]

        self.assertEqual(matches, self.players)

    def test_statistics_matches_parsed_query(self):
        stats = Statistics(FakeReader(self.players))

        matches = stats.matches(parse("team = NYR and goals >= 10 and goals < 20"))

        self.assertEqual(matches, [self.nyr_medium])

    def test_points_attribute_uses_player_property(self):
        matcher = parse("points >= 20")

        matches = [player for player in self.players if matcher.test(player)]

        self.assertIn(self.nyr_medium, matches)
        self.assertIn(self.nyr_high, matches)
        self.assertIn(self.edm, matches)
        self.assertNotIn(self.nyr_low, matches)

    def test_invalid_attribute_raises_value_error(self):
        with self.assertRaises(ValueError):
            parse("name >= 10")

    def test_invalid_number_raises_value_error(self):
        with self.assertRaises(ValueError):
            parse("goals >= ten")

    def test_empty_condition_raises_value_error(self):
        with self.assertRaises(ValueError):
            parse("team = NYR and")


if __name__ == "__main__":
    unittest.main()
