# from config.aws_boto3 import boto3Client
import boto3
from boto3.dynamodb.conditions import Attr, Key
from config.setting import setting

class dynamodb:
    def __init__(self) -> None:
        self.resource = boto3.resource(
            'dynamodb',
            # endpoint_url='http://localhost:8001',
            aws_access_key_id = setting.role_aws_key,
            aws_secret_access_key = setting.role_aws_secret,
            region_name=setting.region_name
        )

    def table(self, table_name:str):
        table = self.resource.Table(table_name)
        return table