# Generated by Django 3.0.4 on 2023-06-27 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_booking_granted'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='revoked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='grantedbookings',
            name='revoked',
            field=models.BooleanField(default=False),
        ),
    ]