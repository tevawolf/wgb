# Generated by Django 2.1.3 on 2018-12-06 07:55

import WGB.models
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('WGB', '0025_auto_20181206_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directmessage',
            name='send_datetime',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 6, 7, 55, 54, 58000, tzinfo=utc), verbose_name='送信日時'),
        ),
        migrations.AlterField(
            model_name='directmessageattachment',
            name='attachment',
            field=models.ImageField(blank=True, null=True, upload_to=WGB.models.get_upload_to, verbose_name='添付ファイル'),
        ),
        migrations.AlterField(
            model_name='threads',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 6, 7, 55, 54, 56000, tzinfo=utc), verbose_name='作成日時'),
        ),
        migrations.AlterField(
            model_name='threadwrite',
            name='write_datetime',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 6, 7, 55, 54, 57000, tzinfo=utc), verbose_name='書き込み日時'),
        ),
        migrations.AlterField(
            model_name='threadwriteattachment',
            name='attachment',
            field=models.ImageField(blank=True, null=True, upload_to=WGB.models.get_upload_to, verbose_name='添付画像ファイル'),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to=WGB.models.get_upload_to, verbose_name='アイコン画像パス'),
        ),
    ]
