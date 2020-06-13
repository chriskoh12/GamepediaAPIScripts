# Function to check if a team/player exists in a dynamodb table
# Determines if the entity is in the table by checking if
# the response(which is of type dict) has key "Item", which means item exists
# args:
# table - boto3 table resource
# entity_name - name of player to check
#
# returns true if player in the table, otherwise false


def check_entity_in_table(table, entity_name):
    try:
        response = table.get_item(
            Key={
                'Name': entity_name
            }
        )
    except Exception as e:
        print("Error while trying to check if an entity exists. Is the table name spelled correctly? ")

    return bool("Item" in response)
