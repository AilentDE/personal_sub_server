import smtplib
from email.mime.text import MIMEText

def send_test(target:str)
    # test smtp mail

def send_mail(target:str, body:str, feature: dict, subject:str = "來自可洛斯的通知"):
    msg = body
    for el in feature.keys():
        msg = msg.replace("{{"+str(el)+"}}", str(feature[el]))
    mail = MIMEText(msg, 'html', 'utf-8')
    mail['Subject'] = subject
    mail['From'] = 'service@clusters.tw'
    mail['To'] = target

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('clusters_info@clusters.tw', os.environ['MAIL_PASS'])
    try:
        status = smtp.sendmail('service@clusters.tw', target, mail.as_string())
    except Exception as error:
        smtp.quit()
        return {
            "success": False,
            "message": '信件寄送失敗了',
            "detail": f'{error}'
        }
    smtp.quit()
    return {
        "success": True,
        "message": '信件寄出成功'
    }

async def send_notification(target:str, body:str, feature: dict, subject:str = "來自可洛斯的通知"):
    msg = body
    for el in feature.keys():
        msg = msg.replace("{{"+str(el)+"}}", str(feature[el]))
    mail = MIMEText(msg, 'html', 'utf-8')
    mail['Subject'] = subject
    mail['From'] = 'service@clusters.tw'
    mail['To'] = target

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('clusters_info@clusters.tw', os.environ['MAIL_PASS'])
    try:
        status = smtp.sendmail('service@clusters.tw', target, mail.as_string())
    except Exception as error:
        smtp.quit()
        return {
            "success": False,
            "message": '信件寄送失敗了',
            "detail": f'{error}'
        }
    smtp.quit()
    return {
        "success": True,
        "message": '信件寄出成功'
    }