# Generated by Django 2.1.3 on 2018-11-26 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WGB', '0001_initial'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='accountsub',
        #     name='icon',
        #     field=models.ImageField(upload_to='C:\\Users\\i1457\\WGB\\static/uploads/icons/', verbose_name='アイコン画像パス'),
        # ),
        migrations.AlterField(
            model_name='directmessageattachment',
            name='attachment',
            field=models.FileField(upload_to='C:\\Users\\i1457\\WGB\\static/uploads/attachment_messages/', verbose_name='添付ファイル'),
        ),
        migrations.AlterField(
            model_name='threadwriteattachment',
            name='attachment',
            field=models.FileField(upload_to='C:\\Users\\i1457\\WGB\\static/uploads/attachments/', verbose_name='添付ファイル'),
        ),
    ]
