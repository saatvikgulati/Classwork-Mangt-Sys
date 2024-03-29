# Generated by Django 3.1.4 on 2021-01-14 11:57

import assignment.validators
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0006_auto_20210114_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='expires_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 15, 11, 57, 18, 349886, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='pdf',
            field=models.FileField(default='sample.pdf', upload_to='assignments', validators=[assignment.validators.validate_file_extension]),
        ),
    ]
