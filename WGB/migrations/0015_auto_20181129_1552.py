# Generated by Django 2.1.3 on 2018-11-29 06:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
from django.utils.timezone import now


class Migration(migrations.Migration):

    dependencies = [
        ('WGB', '0014_auto_20181128_1732'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='threadwrite',
            options={'get_latest_by': 'number', 'verbose_name': '掲示板書き込み', 'verbose_name_plural': '2.掲示板書き込み'},
        ),
        migrations.AlterField(
            model_name='threads',
            name='create_date',
            field=models.DateTimeField(default=now, verbose_name='作成日時'),
        ),
        migrations.AlterField(
            model_name='threadwrite',
            name='write_datetime',
            field=models.DateTimeField(default=now, verbose_name='書き込み日時'),
        ),
    ]
