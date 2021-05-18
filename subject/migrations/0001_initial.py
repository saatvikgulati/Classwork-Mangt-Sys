# Generated by Django 3.0.8 on 2020-07-17 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(choices=[('VAVR', 'Verification and validtion tehcniques'), ('DWDM', 'Datawarehousing and data mining '), ('DTSC1', 'Introduction to data science '), ('COA', 'Computer Organisation and Architecture'), ('Mup', 'Micro Controller and Processor'), ('WebT', 'Web Technologies'), ('ST', 'Statistics')], default='VAVR', max_length=25)),
                ('lectures', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('course', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='course.Course')),
            ],
        ),
    ]