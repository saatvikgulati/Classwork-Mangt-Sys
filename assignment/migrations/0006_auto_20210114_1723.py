# Generated by Django 3.1.4 on 2021-01-14 11:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0005_auto_20210114_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='expires_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 15, 11, 53, 39, 110542, tzinfo=utc)),
        ),
    ]