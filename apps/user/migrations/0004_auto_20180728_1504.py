# Generated by Django 2.0.7 on 2018-07-28 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20180728_0955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='base_add',
        ),
        migrations.AddField(
            model_name='address',
            name='detail',
            field=models.CharField(default='', max_length=256, verbose_name='详细地址'),
        ),
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(default='', max_length=300, verbose_name='基础地址'),
        ),
    ]