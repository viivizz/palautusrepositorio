"""Laske pelaajia koskevia arvoja."""

class PlayerStats:
    """Kasittele tilastoja."""
    def __init__(self, reader):
        """Alustaa tilastot hakemalla tietoa lukijalta."""
        self.reader=reader

    def top_scores_by_nationality(self, nationality):
        """Palauttaa tietyn kansallisuuden pelaajat järjestyksessä."""
        players=self.reader.get_players()

        nationality_players=[]

        for player in players:
            if player.nationality==nationality:
                nationality_players.append(player)

        sorted_players=sorted(nationality_players, key=lambda player: player.goals+player.assists, reverse=True)

        return sorted_players

    def top_scores_by_team(self, team):
        """Palauttaa tietyn joukkueen pelaajat pisteiden mukaan järjestettynä."""
        players=self.reader.get_players()

        team_players=[]

        for player in players:
            if player.team==team:
                team_players.append(player)

        sorted_players=sorted(
            team_players,
            key=lambda player: (player.goals + player.assists, player.goals),
            reverse=True,
        )

        return sorted_players

    def top_goal_scorers(self, how_many):
        """Palauttaa how_many eniten maaleja tehnyttä pelaajaa maalimäärän mukaan laskevassa järjestyksessä"""
        players=self.reader.get_players()
        sorted_players=sorted(players, key=lambda player: player.goals, reverse=True)
        return sorted_players[:how_many]
