# Generated by Django 2.1.3 on 2018-11-30 06:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('WGB', '0018_auto_20181130_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='threads',
            name='password_require',
            field=models.BooleanField(default=1, verbose_name='掲示板の参加にパスワード入力必須'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='threads',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 30, 6, 55, 38, 290000, tzinfo=utc), verbose_name='作成日時'),
        ),
        migrations.AlterField(
            model_name='threadwrite',
            name='write_datetime',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 30, 6, 55, 38, 291000, tzinfo=utc), verbose_name='書き込み日時'),
        ),
        migrations.AlterUniqueTogether(
            name='directmessage',
            unique_together={('thread', 'from_member', 'to_member')},
        ),
    ]
