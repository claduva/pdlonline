# Generated by Django 3.1.7 on 2021-03-23 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league_configuration', '0011_auto_20210323_0016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='league_pokemon',
            name='points',
        ),
        migrations.AlterField(
            model_name='league_pokemon',
            name='tier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league_configuration.league_tier'),
        ),
    ]
