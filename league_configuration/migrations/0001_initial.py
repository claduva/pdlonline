# Generated by Django 3.1.7 on 2021-03-17 03:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='league',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('abbreviviation', models.CharField(max_length=10)),
                ('logo', models.URLField(blank=True, default='https://media.discordapp.net/attachments/821585145961644062/821585187062153216/genericleague.png', max_length=400)),
                ('platform', models.CharField(choices=[('Youtube Showdown', 'Youtube Showdown'), ('Youtube Wifi', 'Youtube Wifi'), ('Showdown', 'Showdown'), ('Wifi', 'Wifi')], default='Showdown', max_length=30)),
                ('status', models.CharField(choices=[('In Season', 'In Season'), ('Inactive', 'Inactive'), ('Recruiting Coaches', 'Recruiting Coaches'), ('In Offseason', 'In Offseason')], default='Inactive', max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('host', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]