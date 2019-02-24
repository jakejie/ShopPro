# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:JakeBlog
FileName = PyCharm
Version:1.0
CreateDay:2018/3/23 16:38
"""
from random import Random
from django.core.mail import send_mail
from ShopPro.settings import EMAIL_FROM, HOST
from user.models import EmailVerifyRecord
# from celery import Celery

# celery = Celery("tasks", broker="redis://{}:6379/0".format(REDIS_HOST),
#                 backend="redis://{}:6379/0".format(REDIS_HOST))

# celery = Celery("tasks", broker="redis://127.0.0.1:6379/0",
#                 backend="redis://127.0.0.1:6379/0")


# 注册用户/找回密码 发送验证邮件
# @celery.task
def sent_register_email(email, sent_type='register'):
    # email = data[0]
    # sent_type = data[1]
    email_record = EmailVerifyRecord()
    code = random_str(32)
    email_record.code = code
    email_record.email = email
    email_record.sent_type = sent_type
    email_record.save()
    # 发送邮件
    if sent_type == "register":
        email_title = "注册用户在线激活链接"
        email_body = "点击以下链接激活你的账号：{}/user/activate/?code={}".format(HOST, code)
        # print("内容准备完成 发送")
        # 主题 内容 发件人 收件人(列表)
        sent_status = send_mail(email_title, email_body, EMAIL_FROM, [email], fail_silently=False)
        if sent_status:
            pass
        # print("sent success")
        pass

    elif sent_type == "forget":
        email_title = "密码重置链接"
        email_body = "点击以下链接重置你的密码：{}/user/reset/password/?code={}".format(HOST, code)
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
