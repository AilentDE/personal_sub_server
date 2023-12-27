from fastapi import HTTPException, Path, Header
import hmac
from hashlib import sha1
from datetime import datetime
from config.aws_boto3 import boto3Client
from config.setting import setting

def write_log(message: str, log_file:str='log.txt'):
    with open('logs/' + log_file, mode='a', encoding='utf-8') as log:
        log.write(f'[{datetime.utcnow()}] ' + message)

def write_log_s3(message:str, file_key:str='logs/log.txt', bucket_name:str=setting.s3_bucket_name):
    client = boto3Client('s3')
    try:
        # 檢查檔案是否存在，如果不存在，則創建一個新檔案
        client.head_object(Bucket=bucket_name, Key=file_key)
    except:
        client.put_object(Bucket=bucket_name, Key=file_key, Body='')
    
    response = client.get_object(Bucket=bucket_name, Key=file_key)
    current_content = response['Body'].read().decode('utf-8')

    updated_content = current_content + '\n' + f'[{datetime.utcnow()}] ' + message

    client.put_object(Bucket=bucket_name, Key=file_key, Body=updated_content)

def check_hmac(
        creator_id: str = Path(..., description="creator_id from path"),
        x_signature: str = Header(..., description="Signature from header")
        ):
    key = setting.hmac_key
    hmac_code = hmac.new(key.encode(), creator_id.encode(), sha1).hexdigest()
    if hmac_code != x_signature:
        raise HTTPException(
            status_code=401,
            detail='validation failed.'
        )
    return creator_id