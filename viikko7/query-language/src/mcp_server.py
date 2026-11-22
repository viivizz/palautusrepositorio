from mcp.server.mcpserver import MCPServer
from statistics import Statistics
from player_reader import PlayerReader
from query_parser import parse
from pathlib import Path

LOG_FILE = Path(__file__).parent.parent / "mcp.log"


def log(message: str):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        print(message, file=file)

URL = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players.txt"

stats = Statistics(PlayerReader(URL))

mcp = MCPServer("NHL-tilastot")


@mcp.tool()
def top_scorers(how_many: int) -> list[str]:
    """Return the players with the most points in the NHL 2024-25 season."""
    log(f"top_scorers called: how_many={how_many}")
    return [str(player) for player in stats.top_scorers(how_many)]


@mcp.tool()
def team_players(team: str) -> list[str]:
    """
    Return all NHL players belonging to the given team.

    The team must be given as a three-letter team code,
    for example NYR, EDM or BOS.
    """
    log(f"team_players called: team={team}")
    matcher = parse(f"team = {team}")
    players = stats.matches(matcher)
    return [str(player) for player in players]


@mcp.tool()
def query_players(query: str) -> list[str]:
    """
    Search NHL players using the query language.

    Supported query syntax:
    - team = XXX: player belongs to team XXX
    - goals >= N: at least N goals
    - goals < N: fewer than N goals
    - assists >= N: at least N assists
    - assists < N: fewer than N assists
    - points >= N: at least N points
    - points < N: fewer than N points
    - and: all connected conditions must match
    - or: at least one condition must match

    AND has higher precedence than OR.

    Example:
    team = NYR and goals >= 10 and goals < 20
    """
    log(f"query_players called: query={query}")
    matcher = parse(query)
    players = stats.matches(matcher)
    return [str(player) for player in players]



if __name__ == "__main__":
    mcp.run()


