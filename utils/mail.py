# import smtplib
import aiosmtplib 
from email.mime.text import MIMEText
from config.setting import setting
from config.aws_boto3 import boto3Client
from dependencies.base import write_log, write_log_s3
from utils.aws_tool import create_presigned_url

def get_template(template_file:str='templates/sample_template.txt')->str:
    with open(template_file, 'r', encoding='utf-8') as template:
        body = template.read()
    return body

async def send_test(target_email:str, msg:str=get_template(), subject:str='Notification from clusters', isSSL:bool=False, isTLS:bool=False):
    # mail
    mail = MIMEText(msg, 'html', 'utf-8')
    mail['Subject'] = subject
    # smtp
    smtp = aiosmtplib.SMTP(hostname='smtp.gmail.com', port=587, use_tls=isSSL)
    await smtp.connect()
    if isTLS:
        await smtp.starttls()
    await smtp.login(setting.smtp_user, setting.smtp_code)
    try:
        await smtp.sendmail(setting.smtp_from, target_email, mail.as_string())
    except Exception as error:
        write_log(f"{error}", 'mail.txt')
    finally:
        await smtp.quit()

async def send_format_mail(target_email:str, subject:str, format_dict:dict, msg:str=get_template(), isSSL:bool=False, isTLS:bool=False):
    # mail
    # msg = msg.format_map(format_dict)
    for key, value in format_dict.items():
        msg = msg.replace('{'+key+'}', value)
    mail = MIMEText(msg, 'html', 'utf-8')
    mail['Subject'] = subject
    # smtp
    smtp = aiosmtplib.SMTP(hostname='smtp.gmail.com', port=587, use_tls=isSSL)
    await smtp.connect()
    if isTLS:
        await smtp.starttls()
    await smtp.login(setting.smtp_user, setting.smtp_code)
    try:
        await smtp.sendmail(setting.smtp_from, target_email, mail.as_string())
    except Exception as error:
        write_log(f"{error}", 'mail.txt')
    finally:
        await smtp.quit()

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
        thumbnail_url = create_presigned_url(setting.s3_bucket_name, format_dict['thumbnail_object'])
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