import smtplib
from email.mime.text import MIMEText
from config.setting import get_settings


def send_test(target_email:str):

    with open('mail_template.txt', 'r', encoding='utf-8') as tmplate:
        msg = tmplate.read()
    mail = MIMEText(msg, 'html', 'utf-8')
    mail['Subject'] = 'subject-test-mail'

    # test smtp mail
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(get_settings().smtp_user, get_settings().smtp_code)
    try:
        response = smtp.sendmail(get_settings().smtp_from, target_email, mail.as_string())
    except Exception as error:
        print(f"{error}")
    finally:
        smtp.quit()


# def send_mail(target:str, body:str, feature: dict, subject:str = "來自可洛斯的通知"):
#     msg = body
#     for el in feature.keys():
#         msg = msg.replace("{{"+str(el)+"}}", str(feature[el]))
#     mail = MIMEText(msg, 'html', 'utf-8')
#     mail['Subject'] = subject
#     mail['From'] = 'service@clusters.tw'
#     mail['To'] = target

#     smtp = smtplib.SMTP('smtp.gmail.com', 587)
#     smtp.ehlo()
#     smtp.starttls()
#     smtp.login('clusters_info@clusters.tw', os.environ['MAIL_PASS'])
#     try:
#         status = smtp.sendmail('service@clusters.tw', target, mail.as_string())
#     except Exception as error:
#         smtp.quit()
#         return {
#             "success": False,
#             "message": '信件寄送失敗了',
#             "detail": f'{error}'
#         }
#     smtp.quit()
#     return {
#         "success": True,
#         "message": '信件寄出成功'
#     }

# async def send_notification(target:str, body:str, feature: dict, subject:str = "來自可洛斯的通知"):
#     msg = body
#     for el in feature.keys():
#         msg = msg.replace("{{"+str(el)+"}}", str(feature[el]))
#     mail = MIMEText(msg, 'html', 'utf-8')
#     mail['Subject'] = subject
#     mail['From'] = 'service@clusters.tw'
#     mail['To'] = target

#     smtp = smtplib.SMTP('smtp.gmail.com', 587)
#     smtp.ehlo()
#     smtp.starttls()
#     smtp.login('clusters_info@clusters.tw', os.environ['MAIL_PASS'])
#     try:
#         status = smtp.sendmail('service@clusters.tw', target, mail.as_string())
#     except Exception as error:
#         smtp.quit()
#         return {
#             "success": False,
#             "message": '信件寄送失敗了',
#             "detail": f'{error}'
#         }
#     smtp.quit()
#     return {
#         "success": True,
#         "message": '信件寄出成功'
#     }