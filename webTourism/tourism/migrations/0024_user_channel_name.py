# Generated by Django 4.2.6 on 2023-10-24 14:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tourism", "0023_rename_location_rating_location_location_rating"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="channel_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]