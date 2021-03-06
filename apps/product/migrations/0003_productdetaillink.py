# Generated by Django 2.0.7 on 2018-07-27 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20180714_1406'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDetailLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('china_book_url', models.CharField(max_length=512, verbose_name='中国图书网平台链接')),
                ('dang_dang_url', models.CharField(max_length=512, verbose_name='当但平台链接')),
                ('jing_dong_url', models.CharField(max_length=512, verbose_name='京东平台链接')),
                ('tian_mao_url', models.CharField(max_length=512, verbose_name='天猫平台链接')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product', verbose_name='关联商品')),
            ],
            options={
                'verbose_name': '商品地址',
                'verbose_name_plural': '商品地址',
            },
        ),
    ]
