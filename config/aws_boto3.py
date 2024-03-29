import boto3
from config.setting import setting

def boto3Client(service:str='s3'):
    '''
    Choose service to use.

    default is AWS S3
    '''
    client = boto3.client(
        service,
        # aws_access_key_id=setting.aws_access_key_id,
        # aws_secret_access_key=setting.aws_secret_access_key,
        # aws_session_token = setting.aws_session_token,
        aws_access_key_id = setting.role_aws_key,
        aws_secret_access_key = setting.role_aws_secret,
        region_name=setting.region_name
    )
    return client