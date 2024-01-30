from config.aws_boto3 import boto3Client
from botocore.exceptions import ClientError
from config.setting import setting
from dependencies.base import get_template
from datetime import datetime
import logging

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

def create_presigned_url(bucket_name:str, object_name:str, expiration:int = 3600, for_download:bool = False) -> str|None:
    """Generate a presigned URL to share an S3 object

    :param expiration: Time in seconds for the presigned URL to remain valid
    :param for_download: Use attachment header or not
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    session = boto3Client('s3')
    try:
        if for_download:
            Params={
                'Bucket': bucket_name,
                'Key': object_name,
                'ResponseContentDisposition': f"attachment; filename = file.jpg"
            }
        else:
            Params={
                'Bucket': bucket_name,
                'Key': object_name
            }
        response = session.generate_presigned_url('get_object',
                                                    Params,
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

def send_test_ses(target_email:str, msg:str=get_template('templates/when_create_work.html'), subject:str='Notification from clusters'):
    client = boto3Client('ses')

    response = client.send_email(
        Source=setting.ses_sender,
        Destination={
            'ToAddresses': [target_email]
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': 'This is the test mail.',
                },
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': msg
                }
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        }
    )
    write_log_s3("Email Sent Successfully. MessageId is: " + response['MessageId'], 'logs/mail.txt')

def send_format_mail_ses(target_email:str, subject:str, format_dict:dict, msg:str=get_template('templates/when_create_work.html')):
    # 處理作品封面圖片連結
    if format_dict['thumbnail_object']:
        thumbnail_url = create_presigned_url('clusters-assets-bucket', format_dict['thumbnail_object'], 7*24*60*60)
        if thumbnail_url:
            format_dict['thumbnail_URL'] = thumbnail_url

    client_ses = boto3Client('ses')

    format_dict.pop('thumbnail_object')
    for key, value in format_dict.items():
        msg = msg.replace('${'+key+'}', value)

    response = client_ses.send_email(
        Source=setting.ses_sender,
        Destination={
            'ToAddresses': [target_email]
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': 'Here is a new work {} from {}.'.format(format_dict['work_url'], format_dict['creator_name']),
                },
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': msg
                }
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        }
    )
    # write_log_s3("Email Sent Successfully. MessageId is: " + response['MessageId'], 'logs/mail.txt')
    # use CloudWatch logs for Exception