from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
from flask import Flask, jsonify, request

# Connect to yahoo api 
sc = OAuth2(None, None, from_file='oauth2.json')

# Get GAME object (which refers to leagues? lol)
gm = yfa.Game(sc, 'nhl')

# Get list of all 'leagues' you've played in
# Each 'league' represents one fantasy season
# This will have to be updated yearly
leagues = gm.league_ids()

# Get the league object
last_years_lg = gm.to_league('419.l.37862')
# this_years_lg = gm.to_league('427.l.14776')

# Get the team key
team_key = last_years_lg.team_key()

# Get the team object
my_team = last_years_lg.to_team(team_key)

# Get team roster
roster = my_team.roster()

print(roster)


# Get opponent's team id for a given week 
# my_team.matchup() # Example Return Value => 388.l.27081.t.9

# Get Free Agents For A League
# Must supply Postion as a string
# last_years_lg.free_agents('C')

# Get player stats for a specified time period
# player_ids = list of ints
# req_type = 'season', 'average_season', 'lastweek', 'lastmonth', 'date', 'week'. 'season'
# Example => lg.player_stats([6743], 'season')
# last_years_lg.player_stats()

# Get Transactions
# trans_types => add,drop,commish,trade
# last_years_lg.(transactions())

# Get league standings
# Returns a list of all teams, index 0 = 1st place
# last_years_lg.standings()

app = Flask(__name__)
print("SERVER IS RUNNING...")


@app.route("/standings", methods=["GET"])
def GetStandings():
  standings = last_years_lg.standings()
  return jsonify(standings)


@app.route("/chat", methods=["GET"])
def chat():
    return jsonify({"a": 1, "b": 2})


if __name__ == "__main__":
    app.run(debug=True)
