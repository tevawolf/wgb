# Generated by Django 2.1.3 on 2018-11-27 05:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        # ('admin', '0004_auto_20181127_1401'),
        # ('auth', '0009_alter_user_last_name_max_length'),
        ('WGB', '0004_auto_20181127_1343'),
    ]

    operations = [
        # migrations.RenameModel(
        #     old_name='Account',
        #     new_name='UserAccount',
        # ),
        migrations.AlterField(
            model_name='directmessage',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, to_field='id', verbose_name='参加メンバー'),
        ),
        migrations.AlterField(
            model_name='threadmember',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, to_field='id', verbose_name='参加メンバー'),
        ),
        migrations.AlterField(
            model_name='threadwrite',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, to_field='id', verbose_name='参加メンバー'),
        ),
        # migrations.AlterModelTable(
        #     name='useraccount',
        #     table='user_account',
        # ),
    ]
