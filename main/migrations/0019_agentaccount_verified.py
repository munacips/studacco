# Generated by Django 3.0.4 on 2023-06-28 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20230628_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentaccount',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]