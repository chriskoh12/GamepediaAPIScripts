import mwclient
import boto3
import sys
from check_entity_in_table import *
from insert_blank_entity import *
from insert_single_entity_stats import *
from parse_unique_line import *


# Insert the stats of teams into their corresponding week/day, looking at all the entries between two dates
# args:
# table_name - the name of the table insert into
# from_date - the beginning date to look at team data in the format yyyy-mm-dd 00:00:00
# to_date - the end date to look at team data
def insert_multiple_team_stats(table_name, from_date, to_date):
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table(table_name)

    site = mwclient.Site('lol.gamepedia.com', path='/')
    response = site.api('cargoquery',
                        limit='500',  # 500 is the max amount of entries returned
                        tables="ScoreboardGames=SG",
                        fields="SG.Team1, SG.Team2, SG.Team1Score, SG.Team1Dragons, SG.Team2Dragons, SG.Team1Barons, SG.Team2Barons, "
                               "SG.Team1Towers, SG.Team2Towers, SG.Team1RiftHeralds, SG.Team2RiftHeralds, SG.Gamelength_Number, SG.UniqueLine",
                        where="SG.OverviewPage = 'LCS/2019 Season/Spring Season' AND SG.DateTime_UTC BETWEEN '" + from_date + "' AND '" + to_date + "' ",
                        order_by="SG.DateTime_UTC"
                        )
    # Get rid of some extra data sent with the response
    response = next(iter(response.items()))
    response = response[1]
    if len(response) == 500:
        print("Maximum query limit reached. Reduce time range so that number of results returned is less than 500.")
        sys.exit(1)

    for entry in response:
        data = entry['title']  # data is now the object with dragons, barons, towers, etc

        unique_line = data['UniqueLine']  # Extract UniqueLine from the response
        week, day = parse_unique_line(unique_line)  # Extract the week and the day of the game
        game_length = data['Gamelength Number']
        winner = bool(int(data['Team1Score']))  # winner is 1 if Team1 won, 0 if Team2 won, have to convert because given as string

        # Get data for team 1
        t1_name = data['Team1']
        t1_drags = data['Team1Dragons']
        t1_barons = data['Team1Barons']
        t1_towers = data['Team1Towers']

        # Get data for team 2
        t2_name = data['Team2']
        t2_drags = data['Team2Dragons']
        t2_barons = data['Team2Barons']
        t2_towers = data['Team2Towers']

        # Call helper function to insert both teams' stats
        insert_single_team_stats(t1_name, winner, game_length, t1_drags, t1_barons, t1_towers, week, day, table)
        insert_single_team_stats(t2_name, not winner, game_length, t2_drags, t2_barons, t2_towers, week, day, table)


# Helper function to reduce code duplication and insert a single team's stats
# args:
# name - name of team
# win - whether the team won or not, as a bool
# drags, barons, towers - how many of each the team got
# week, day - the week and day of the split the game took place
# table - the dynamodb table to insert into
def insert_single_team_stats(name, win, game_length, drags, barons, towers, week, day, table):
    in_dynamo = check_entity_in_table(table, name)  # Check if the entity has an entry in dynamo
    if not in_dynamo:  # If entity is not already in the table, insert a placeholder
        insert_blank_entity(table, name)

    stats = {
        "Victory": win,
        "GameLength": game_length,
        "Dragons": drags,
        "Barons": barons,
        "Towers": towers,
        "FirstBlood": bool(False)
    }

    insert_single_entity_stats(table, name, week, day, stats)


insert_multiple_team_stats('TeamStats2019Spring', "2019-01-23", "2019-01-30")
