# Generated by Django 3.1.7 on 2021-04-15 14:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0010_auto_20210410_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='expires_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 16, 14, 0, 40, 376693, tzinfo=utc)),
        ),
    ]