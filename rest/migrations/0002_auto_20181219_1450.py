# Generated by Django 2.1.4 on 2018-12-19 22:50

from django.db import migrations, models
import rest.validators


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='short_name',
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=60, unique=True, validators=[rest.validators.validate_course_name], verbose_name='Course Title'),
        ),
    ]
