# from config.aws_boto3 import boto3Client
import boto3
from boto3.dynamodb.conditions import Attr, Key
from config.setting import setting

class dynamodb:
    def __init__(self) -> None:
        self.resource = boto3.resource(
            'dynamodb',
            endpoint_url='http://localhost:8001',
            aws_access_key_id = 'fake',
            aws_secret_access_key = 'fake',
            region_name='ap-northeast-1')

    def table(self, table_name:str):
        table = self.resource.Table(table_name)
        return table