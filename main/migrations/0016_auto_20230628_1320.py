# Generated by Django 3.0.4 on 2023-06-28 11:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0015_auto_20230628_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='room',
            field=models.ForeignKey(on_delete=models.SET('deleted'), to='main.Room'),
        ),
        migrations.AlterField(
            model_name='grantedbookings',
            name='agent',
            field=models.ForeignKey(on_delete=models.SET('deleted'), to='main.AgentAccount'),
        ),
        migrations.AlterField(
            model_name='houserating',
            name='rater',
            field=models.ForeignKey(on_delete=models.SET('deleted'), to=settings.AUTH_USER_MODEL),
        ),
    ]