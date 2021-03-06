# Generated by Django 3.1.7 on 2021-03-31 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league_configuration', '0020_discord_settings'),
        ('leagues', '0002_auto_20210331_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='league_configuration.league'),
        ),
    ]
