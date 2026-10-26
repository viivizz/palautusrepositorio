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
