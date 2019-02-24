from celery import shared_task
from django.core.mail import send_mail
from random import Random
from ShopPro.settings import EMAIL_FROM, ACTIVATE_HOST, HOST
from user.models import EmailVerifyRecord

from ShopPro.celery import app


# @shared_task
@app.task
def sent_register_email(email, sent_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(32)
    email_record.code = code
    email_record.email = email
    email_record.sent_type = sent_type
    email_record.save()
    # 发送邮件
    if sent_type == "register":
        email_title = "注册用户在线激活链接"
        email_body = "点击以下链接激活你的账号：http://{}/activate/?code={}".format(HOST, code)
        print("新注册用户 发送邮件")
        # 主题 内容 发件人 收件人(列表)
        sent_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if sent_status:
            pass
        print("ok")
        pass
    elif sent_type == "forget":
        print("忘记密码 发送邮件")
        email_title = "密码重置链接"
        email_body = "点击以下链接重置你的密码：http://{}/reset/password/?code={}".format(ACTIVATE_HOST, code)
        # 主题 内容 发件人 收件人(列表)
        sent_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if sent_status:
            pass
    else:
        pass


# 生成随机字符串
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str
