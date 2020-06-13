import mwclient
import boto3

dynamo = boto3.resource('dynamodb')
site = mwclient.Site('lol.gamepedia.com', path='/')

response = site.api('cargoquery',
                    limit='500',
                    # offset='500',
                    tables="ScoreboardPlayers=SP",
                    fields="SP.Name, SP.Kills, SP.Deaths, SP.Assists, SP.CS, SP.Team, SP.UniqueLine, SP.DateTime_UTC, SP.UniqueLine",
                    where="SP.OverviewPage = 'LCS/2019 Season/Spring Season' AND SP.DateTime_UTC BETWEEN '2019-01-23' AND '2019-01-30'"
                    )

# OR SP.OverviewPage = 'LEC/2019 Season/Summer Season'

response = next(iter(response.items()))
response = response[1]
# for i in response:
#     print(json.dumps(i["title"]))

number = 5
stats = {
    "Kills": 1,
    "Deaths": 2,
    "Assists": 19,
    "CS": 100
}

table = dynamo.Table('PlayerKDA2019Spring')

def check_player_in_dynamo(table_name, player_name):
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table(table_name)
    response = table.get_item(
        Key={
            'PlayerName': player_name
        }
    )
    return bool("Item" in response)

print(check_player_in_dynamo('PlayerKDA2019Spring', 'Bjergsenn'))

# response = table.update_item(
#     Key={
#         'PlayerName': 'Bjergsen'
#     },
#     UpdateExpression="SET Weeks[" + str(number) + "] = :new",
#     ExpressionAttributeValues={
#         ':new': stats
#     },
#     ReturnValues="ALL_NEW"
# )


# print(response.Item)

# response = table.update_item(
#     Key={
#         'PlayerName': 'Bjergsen'
#     },
#     UpdateExpression="SET Weeks = list_append(Weeks, :new)",
#     ExpressionAttributeValues={
#         ':new': [{
#             "Kills": 1,
#             "Deaths": 2,
#             "Assists": 4,
#             "CS": 100
#         }]
#     },
#     ReturnValues="ALL_NEW"
# )
# response = table.update_item(
#     Key={
#         'PlayerName': 'Bjergsen'
#     },
#     UpdateExpression="SET val=:var",
#     ExpressionAttributeValues={
#         ':var': 'NotTesty'
#     },
#     ReturnValues="ALL_NEW"
# )
# response = table.put_item(
#     Item={
#         'Name': 'test'
#     }
# )

# print(response)
# for key, value in enumerate(response.items()):
#     print(value)
# print(json.dumps(response, indent=4))
