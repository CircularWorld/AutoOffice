# Generated by Django 2.2.12 on 2020-09-22 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_name', models.CharField(max_length=40, unique=True, verbose_name='企业名')),
                ('email', models.EmailField(default='', max_length=254, unique=True, verbose_name='企业邮箱')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('phone', models.CharField(default='', max_length=11, verbose_name='手机')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
    ]
