# Generated by Django 3.0.8 on 2020-07-17 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('answer', '0001_initial'),
        ('grades', '0002_auto_20200717_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grade',
            name='question_marks',
        ),
        migrations.AddField(
            model_name='grade',
            name='answer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='answer.Answer'),
        ),
    ]
