"""Pelaajia kasitteleva luokka."""

class Player:
    """Havainnolistaa yhden pelaajan tietoja."""

    def __init__(self, player_dict):
        self.name = player_dict['name']
        self.nationality=player_dict['nationality']
        self.team=player_dict['team']
        self.goals=player_dict['goals']
        self.assists=player_dict['assists']

    def __str__(self):
        """Palauttaa pelaajien tiedot."""
        return f"{self.name:20} {self.team:15}{self.goals}+{self.assists}={self.goals+self.assists}"
