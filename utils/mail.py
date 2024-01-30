# import smtplib
import aiosmtplib 
from email.mime.text import MIMEText
from config.setting import setting
from dependencies.base import get_template, write_log

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