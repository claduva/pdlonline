# Generated by Django 3.1.7 on 2021-03-19 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league_configuration', '0005_subleague'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subleague',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subleagues', to='league_configuration.league'),
        ),
    ]
