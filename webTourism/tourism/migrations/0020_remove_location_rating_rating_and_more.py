# Generated by Django 4.2.5 on 2023-10-08 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tourism', '0019_location_created_at_verification_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='rating',
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('comment', models.TextField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='tourism.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='Location_rating',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='tourism.rating'),
        ),
    ]
