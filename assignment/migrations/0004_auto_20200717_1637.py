# Generated by Django 3.0.8 on 2020-07-17 11:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0003_auto_20200717_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='expires_on',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 18, 11, 7, 58, 315184, tzinfo=utc)),
        ),
    ]
