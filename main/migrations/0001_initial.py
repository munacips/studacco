# Generated by Django 3.0.4 on 2023-06-19 16:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allowed_sex', models.CharField(choices=[('m', 'Male'), ('f', 'Female'), ('b', 'Both')], max_length=1)),
                ('location', models.CharField(max_length=50)),
                ('house_address', models.CharField(max_length=200)),
                ('display_picture', models.ImageField(upload_to='dp/houses')),
                ('rating', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=1)),
                ('display_picture', models.ImageField(upload_to='dp/rooms/')),
                ('number_of_beds', models.IntegerField()),
                ('available_beds', models.IntegerField()),
                ('available', models.BooleanField(default=True)),
                ('pricing', models.DecimalField(decimal_places=2, max_digits=8)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.House')),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RoomPic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='pics/rooms/')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Room')),
            ],
        ),
        migrations.CreateModel(
            name='HouseRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.House')),
                ('rater', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HousePic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='pics/houses/')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.House')),
            ],
        ),
        migrations.CreateModel(
            name='HouseFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=100)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.House')),
            ],
        ),
        migrations.AddField(
            model_name='house',
            name='lived_in',
            field=models.ManyToManyField(related_name='lived_in_house', to='main.UserAccount'),
        ),
        migrations.CreateModel(
            name='AgentAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent_name', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]