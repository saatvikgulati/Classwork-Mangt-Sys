# Generated by Django 3.1.3 on 2021-04-30 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sem',
            name='semname',
            field=models.CharField(default='One', max_length=5),
        ),
    ]
