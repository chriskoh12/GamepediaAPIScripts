# Insert stats for a team/player, subtracting 1 from both week and day
# because gamepedia uses 1-based indexing and dynamo uses 0-based
# args:
# table_name - boto3 table resource
# entity_name - name of entity
# week_num - week to insert stats into
# day_num - day of the week to insert stats into
# stats - json object w/stats:
# Kills, Deaths, Assists, CS for a player
# Win, Dragons, Barons, Towers, RiftHeralds, Gamelength
# returns the new value as it appears in the table


def insert_single_entity_stats(table, entity_name, week_num, day_num, stats):
    response = table.update_item(
        Key={
            'Name': entity_name
        },
        # subtract 1 from week and day num because gamepedia returns week and day num with 1-based indexing
        UpdateExpression="SET Weeks[" + str(week_num - 1) + "][" + str(day_num - 1) + "] = :new",
        ExpressionAttributeValues={
            ':new': stats
        },
        ReturnValues="ALL_NEW"
    )

    print("Inserted data for %s from week %d day %d" % (entity_name, week_num, day_num))
    return response

#
# stats_ = {
#     "Kills": 1,
#     "Deaths": 2,
#     "Assists": 4,
#     "CS": 69
# }
# entity_name_ = 'Bjergsen'
# week_num_ = 2
# day_num_ = 2
# table_name_ = 'entityKDA2019Spring'
#
# response_ = insert_single_entity_stats(table_name_, entity_name_, week_num_, day_num_, stats_)
# print(response_)
