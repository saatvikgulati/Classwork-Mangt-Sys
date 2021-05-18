# Generated by Django 3.0.8 on 2020-07-17 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0001_initial'),
        ('subject', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpeg', upload_to='student_profile_pics')),
                ('is_student', models.BooleanField(default=True)),
                ('assigned_course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='course.Course')),
                ('assigned_subject', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='subject.Subject')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
