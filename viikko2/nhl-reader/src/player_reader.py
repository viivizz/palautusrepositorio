"""Etsii pelaajien tiedot palvelimelta."""

import requests
from player import Player

class PlayerReader:
    """Hakee tiedot palvelimelta."""
    def __init__(self,url):
        """Antaa palvelimen osoitteen kaytettavaksi."""
        self.url=url

    def get_players(self):
        """Etsii pelaajat ja palauttaa ne."""
        response=requests.get(self.url, timeout=10).json()

        players=[]

        for player_dict in response:
            player=Player(player_dict)
            players.append(player)

        return players
