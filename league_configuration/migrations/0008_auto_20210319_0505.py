# Generated by Django 3.1.7 on 2021-03-19 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league_configuration', '0007_auto_20210319_0502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='discordserver',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='league',
            name='discordurl',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]