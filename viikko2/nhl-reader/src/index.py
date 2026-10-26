from rich.console import Console
from rich.table import Table
from player_reader import PlayerReader
from player_stats import PlayerStats

def main():
    season=input("Season (for example 2024-25): ")
    nationality=input("Nationality (for example FIN): ")
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader=PlayerReader(url)
    stats=PlayerStats(reader)
    players=stats.top_scores_by_nationality("FIN")

    console=Console()
    table=Table(title=f"Season {season} players from {nationality}")

    table.add_column("Released", style="cyan")
    table.add_column("teams", style="magenta")
    table.add_column("goals", justify="right", style="green")
    table.add_column("assists", justify="right", style="green")
    table.add_column("points", justify="right", style="green")
   

    for player in players:
        points=player.goals+player.assists
        table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(points))

    console.print(table)

if __name__ == "__main__":
    main()
