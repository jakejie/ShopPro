# Generated by Django 2.0.7 on 2018-07-28 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20180728_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logistics',
            name='orderNum',
            field=models.CharField(max_length=32, verbose_name='订单号'),
        ),
    ]