# Generated by Django 2.0.7 on 2018-07-14 14:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerifyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default='', max_length=50, verbose_name='邮箱')),
                ('code', models.CharField(default='', max_length=64, verbose_name='验证码')),
                ('send_type', models.CharField(choices=[('register', '注册'), ('forget', '找回密码')], default='', max_length=10, verbose_name='验证码类型')),
                ('sent_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='邮件发送时间')),
            ],
            options={
                'verbose_name_plural': '邮箱验证码管理',
                'verbose_name': '邮箱验证码管理',
            },
        ),
    ]