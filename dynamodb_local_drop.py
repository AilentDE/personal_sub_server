import boto3
from botocore.exceptions import ClientError
import logging

def drop_table(dyn_resource=None):
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
    try:
        dyn_resource.delete_table(TableName=user_table_name)
    except Exception as err:
        logging.error(f'{err}')
    
    # guild
    guild_table_name = "discordClusters-discordGuild"
    try:
        dyn_resource.delete_table(TableName=guild_table_name)
    except Exception as err:
        logging.error(f'{err}')
    
    return 'Drop table finished.'


if __name__ == "__main__":
    create_state = drop_table()
    print(f"{create_state}")
