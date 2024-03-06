import boto3
from botocore.exceptions import ClientError

def create_table(dyn_resource=None):
    """
    Creates DynamoDB tables for discordClusters project.
    """
    if dyn_resource is None:
        # dyn_resource = boto3.resource("dynamodb")
        dyn_resource = boto3.client(
            'dynamodb',
            endpoint_url='http://localhost:8001',
            aws_access_key_id = 'fake',
            aws_secret_access_key = 'fake',
            region_name='ap-northeast-1'
        )

    # user
    user_table_name = "discordClusters-userData"
    params = {
        "TableName": user_table_name,
        "KeySchema": [
            {"AttributeName": "clustersUserId", "KeyType": "HASH"},
            {"AttributeName": "discordUserId", "KeyType": "RANGE"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "clustersUserId", "AttributeType": "S"},
            {"AttributeName": "discordUserId", "AttributeType": "S"},
        ],
        "ProvisionedThroughput": {"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    }
    try:
        table = dyn_resource.create_table(**params)
        print(f"Creating {user_table_name}...")
        print(table)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table {user_table_name} already exists.")
        else:
            raise
    
    # guild
    guild_table_name = "discordClusters-discordGuild"
    params = {
        "TableName": guild_table_name,
        "KeySchema": [
            {"AttributeName": "guildOwner", "KeyType": "HASH"},
            {"AttributeName": "itemType", "KeyType": "RANGE"},
        ],
        "AttributeDefinitions": [
            {"AttributeName": "guildOwner", "AttributeType": "S"},
            {"AttributeName": "itemType", "AttributeType": "S"},
        ],
        "ProvisionedThroughput": {"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    }
    try:
        table = dyn_resource.create_table(**params)
        print(f"Creating {guild_table_name}...")
        print(table)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table {guild_table_name} already exists.")
        else:
            raise
    
    return 'Init finished.'


if __name__ == "__main__":
    create_state = create_table()
    print(f"{create_state}")
