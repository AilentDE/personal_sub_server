import boto3
from config.setting import setting

def boto3Client(service:str='s3'):
    '''
    Choose service to use.

    default is AWS S3
    '''
    client = boto3.client(
        service,
        aws_access_key_id=setting.aws_access_key_id,
        aws_secret_access_key=setting.aws_secret_access_key,
        aws_session_token = setting.aws_session_token,
        region_name=setting.region_name
    )
    try:
        return client
    finally:
        client.close()