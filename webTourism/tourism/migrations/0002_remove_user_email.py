# Generated by Django 4.2.5 on 2023-09-16 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tourism', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
    ]
