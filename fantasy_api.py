from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
from flask import Flask, jsonify, request
from flask_cors import CORS

# venv/vsCode activate work around
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
global sc
global gm
global leagues
global last_years_lg
global my_team
################### Yahoo Auth/Setup ####################
# Connect to yahoo api 
sc = OAuth2(None, None, from_file='oauth2.json')

# Get GAME object (which refers to leagues? lol)
gm = yfa.Game(sc, 'nhl')

# Get list of all 'leagues' you've played in
# Each 'league' represents one fantasy season
# This will have to be updated yearly
leagues = gm.league_ids()

# Get the league object (must be updated annually, or take last one in list)
last_years_lg = gm.to_league('419.l.37862')
# this_years_lg = gm.to_league('427.l.14776')

# Get the team key
team_key = last_years_lg.team_key()

# Get the team object
my_team = last_years_lg.to_team(team_key)

# Get team roster
roster = my_team.roster()

print(roster)

################### Server ##############################
app = Flask(__name__)
CORS(app)
print("SERVER IS RUNNING...")

################## Routes ###############################
@app.route("/standings", methods=["GET"])
def GetStandings():
  # Get league standings
  # Returns a list of all teams, index 0 = 1st place
  # last_years_lg.standings()
  standings = last_years_lg.standings()
  return jsonify(standings)

@app.route("/roster", methods=["GET"])
def GetMyRoster():
  # Get team roster
  roster = my_team.roster()
  return jsonify(roster)

@app.route("/matchup/<weekId>", methods=["GET"])
def GetMatchup(weekId = 1):
  # Get opponent's team id for a given week 
  # my_team.matchup() # Example Return Value => 388.l.27081.t.9
  matchup = my_team.matchup(weekId)
  return jsonify(matchup)

@app.route("/adds", methods=["GET"])
def GetAdds():
    # Get Transactions
    # trans_types => add,drop,commish,trade
    # count => number of transactions to get
    adds = last_years_lg.transactions('add', '10')
    return jsonify(adds)

@app.route("/drops", methods=["GET"])
def GetDrops():
    # Get Transactions
    # trans_types => add,drop,commish,trade
    # count => number of transactions to get
    drops = last_years_lg.transactions('drop', '10')
    return jsonify(drops)

@app.route("/freeAgents/<position>", methods=["GET"])
def GetFreeAgents(position):
    # Get Free Agents For A League
    # Must supply Postion as a string
    free_agents = last_years_lg.free_agents(position)
    return jsonify(free_agents)

@app.route("/stats/season/<stringOfPlayerIds>", methods=["GET"])
def GetPlayerStatsForSeason(stringOfPlayerIds):
    # Get player stats for a specified time period
    # player_ids = list of ints
    # req_type = 'season', 'average_season', 'lastweek', 'lastmonth', 'date', 'week'. 'season'
    # Example => lg.player_stats([6743], 'season')
    stats = last_years_lg.player_stats([stringOfPlayerIds], 'season')
    return jsonify(stats)

@app.route("/stats/seasonAverage/<stringOfPlayerIds>", methods=["GET"])
def GetPlayerStatsForSeasonAverage(stringOfPlayerIds):
    # Get player stats for a specified time period
    # player_ids = list of ints
    # req_type = 'season', 'average_season', 'lastweek', 'lastmonth', 'date', 'week'. 'season'
    # Example => lg.player_stats([6743], 'season')
    stats = last_years_lg.player_stats([stringOfPlayerIds], 'average_season')
    return jsonify(stats)

@app.route("/stats/lastWeek/<stringOfPlayerIds>", methods=["GET"])
def GetPlayerStatsForLastWeek(stringOfPlayerIds):
    # Get player stats for a specified time period
    # player_ids = list of ints
    # req_type = 'season', 'average_season', 'lastweek', 'lastmonth', 'date', 'week'. 'season'
    # Example => lg.player_stats([6743], 'season')
    stats = last_years_lg.player_stats([stringOfPlayerIds], 'lastweek')
    return jsonify(stats)

@app.route("/stats/lastMonth/<stringOfPlayerIds>", methods=["GET"])
def GetPlayerStatsForLastMonth(stringOfPlayerIds):
    # Get player stats for a specified time period
    # player_ids = list of ints
    # req_type = 'season', 'average_season', 'lastweek', 'lastmonth', 'date', 'week'. 'season'
    # Example => lg.player_stats([6743], 'season')
    stats = last_years_lg.player_stats([stringOfPlayerIds], 'lastmonth')
    return jsonify(stats)

@app.route("/stats/currentDate/<stringOfPlayerIds>", methods=["GET"])
def GetPlayerStatsForToday(stringOfPlayerIds):
    # Get player stats for a specified time period
    # player_ids = list of ints
    # req_type = 'season', 'average_season', 'lastweek', 'lastmonth', 'date', 'week'. 'season'
    # Example => lg.player_stats([6743], 'season')
    stats = last_years_lg.player_stats([stringOfPlayerIds], 'date')
    return jsonify(stats)

#############################################################

if __name__ == "__main__":
    app.run(debug=True)
