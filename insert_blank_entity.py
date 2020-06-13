# Insert a blank team/player into given table
# with their name and an empty size 9 array to store weekly stats
# args:
# table_name - boto3 table resource
# entity_name - name of team/player to be inserted
# returns the new item as it appears after the update in the table


def insert_blank_entity(table, entity_name):
    response = table.put_item(
        Item={
            "Name": entity_name,
            "Weeks": [[{}, {}], [{}, {}], [{}, {}],
                      [{}, {}], [{}, {}], [{}, {}],
                      [{}, {}], [{}, {}], [{}, {}]]
        }
    )

    print("Inserted blank entry for %s" % entity_name)
    return response


# player = 'Bjergsen'
# dynamo_table = 'PlayerKDA2019Spring'
#
# insert_blank_player(dynamo_table, player)
