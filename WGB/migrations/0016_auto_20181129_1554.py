# Generated by Django 2.1.3 on 2018-11-29 06:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('WGB', '0015_auto_20181129_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threads',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 29, 6, 54, 26, 587007, tzinfo=utc), verbose_name='作成日時'),
        ),
        migrations.AlterField(
            model_name='threadwrite',
            name='write_datetime',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 29, 6, 54, 26, 587007, tzinfo=utc), verbose_name='書き込み日時'),
        ),
    ]
