import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
    def test_search_finds_players(self):
        player=self.stats.search("Kurri")
        self.assertEqual(player.name, "Kurri")

    def test_search_does_not_find_player(self):
        player = self.stats.search("Nobody")
        self.assertIsNone(player)

    def test_team_returns_players_from_team(self):
        players = self.stats.team("EDM")
        self.assertEqual(
            [player.name for player in players],
            ["Semenko", "Kurri", "Gretzky"]
        )

    def test_team_returns_empty_list_for_unknown_team(self):
        players = self.stats.team("XXX")
        self.assertEqual(players, [])

    def test_top_returns_players_in_points_order(self):
        players = self.stats.top(2)
        self.assertEqual(
            [player.name for player in players],
            ["Gretzky", "Lemieux", "Yzerman"]
        )

    def test_top_returns_all_players_when_requested(self):
        players = self.stats.top(4)
        self.assertEqual(
            [player.name for player in players],
            ["Gretzky", "Lemieux", "Yzerman", "Kurri", "Semenko"]
        )


if __name__ == "__main__":
    unittest.main()