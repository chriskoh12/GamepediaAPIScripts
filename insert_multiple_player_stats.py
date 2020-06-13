import mwclient
import boto3
import sys
from check_entity_in_table import *
from insert_blank_entity import *
from insert_single_entity_stats import *
from parse_unique_line import *


# Insert the stats of players into their corresponding week/day, looking at all the entries between two dates
# args:
# table_name - the name of the table insert into
# from_date - the beginning date to look at player data in the format yyyy-mm-dd 00:00:00
# to_date - the end date to look at player data
def insert_multiple_player_stats(table_name, from_date, to_date):

    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table(table_name)

    site = mwclient.Site('lol.gamepedia.com', path='/')
    response = site.api('cargoquery',
                        limit='500',  # 500 is the max amount of entries returned
                        tables="ScoreboardPlayers=SP",
                        fields="SP.Name, SP.Kills, SP.Deaths, SP.Assists, SP.CS, SP.Team, SP.UniqueLine, SP.DateTime_UTC, SP.UniqueLine",
                        where="SP.OverviewPage = 'LCS/2019 Season/Spring Season' AND SP.DateTime_UTC BETWEEN '" + from_date + "' AND '" + to_date + "' "
                        )
    # Get rid of some extra data sent with the response
    response = next(iter(response.items()))
    response = response[1]
    if len(response) == 500:
        print("Maximum query limit reached. Reduce time range so that number of results returned is less than 500.")
        sys.exit(1)

    for entry in response:
        data = entry['title']  # data is now the object with kills, deaths, assists, etc
        unique_line = data['UniqueLine']  # Extract UniqueLine from the response
        player_name = data['Name']
        week, day = parse_unique_line(unique_line)  # Extract the week and the day of the game
        in_dynamo = check_entity_in_table(table, player_name)  # Check if the player has an entry in dynamo
        if not in_dynamo:  # If player is not already in the table, insert a placeholder
            insert_blank_entity(table, player_name)

        stats = {
            "Kills": data['Kills'],
            "Deaths": data['Deaths'],
            "Assists": data['Assists'],
            "CS": data['CS'],
            "Multis": [0, 0, 0]
        }

        insert_single_entity_stats(table, player_name, week, day, stats)


insert_multiple_player_stats('PlayerStats2019Spring', "2019-01-23", "2019-01-30")

