# Generated by Django 2.1.3 on 2018-11-27 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WGB', '0005_auto_20181127_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='nickname',
            field=models.CharField(blank=True, max_length=100, verbose_name='ニックネーム'),
        ),
    ]
