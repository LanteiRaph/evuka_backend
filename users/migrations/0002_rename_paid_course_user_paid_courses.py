# Generated by Django 4.0.4 on 2022-04-29 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='paid_course',
            new_name='paid_courses',
        ),
    ]
