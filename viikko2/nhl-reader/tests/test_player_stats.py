from player import Player
from player_stats import PlayerStats


class FakeReader:
    """Stub-lukija, joka palauttaa valmiin pelaajalistan ilman verkkokutsua."""

    def __init__(self, players):
        self._players = players

    def get_players(self):
        return self._players


def test_top_scores_by_nationality_sorts_by_points_descending():
    players = [
        Player({"name": "A", "nationality": "FIN", "team": "TBL", "goals": 10, "assists": 5}),
        Player({"name": "B", "nationality": "SWE", "team": "BOS", "goals": 18, "assists": 7}),
        Player({"name": "C", "nationality": "FIN", "team": "TOR", "goals": 7, "assists": 12}),
        Player({"name": "D", "nationality": "FIN", "team": "NYR", "goals": 15, "assists": 1}),
    ]

    stats = PlayerStats(FakeReader(players))
    result = stats.top_scores_by_nationality("FIN")

    assert [player.name for player in result] == ["C", "D", "A"]
    assert result[0].goals + result[0].assists == 19


def test_top_scores_by_team_sorts_by_points_descending():
    players = [
        Player({"name": "A", "nationality": "FIN", "team": "TBL", "goals": 10, "assists": 5}),
        Player({"name": "B", "nationality": "USA", "team": "TBL", "goals": 8, "assists": 12}),
        Player({"name": "C", "nationality": "FIN", "team": "NYR", "goals": 20, "assists": 2}),
        Player({"name": "D", "nationality": "FIN", "team": "TBL", "goals": 15, "assists": 1}),
    ]

    stats = PlayerStats(FakeReader(players))
    result = stats.top_scores_by_team("TBL")

    assert [player.name for player in result] == ["B", "D", "A"]
    assert result[0].goals + result[0].assists == 20


def test_top_goal_scorers_returns_requested_number():
    players = [
        Player({"name": "A", "nationality": "FIN", "team": "TBL", "goals": 10, "assists": 5}),
        Player({"name": "B", "nationality": "USA", "team": "BOS", "goals": 20, "assists": 3}),
        Player({"name": "C", "nationality": "SWE", "team": "TOR", "goals": 15, "assists": 4}),
    ]

    stats = PlayerStats(FakeReader(players))
    result = stats.top_goal_scorers(2)

    assert [player.name for player in result] == ["B", "C"]
