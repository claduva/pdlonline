# Generated by Django 3.1.7 on 2021-04-02 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league_configuration', '0022_auto_20210402_0405'),
    ]

    operations = [
        migrations.AddField(
            model_name='league_pokemon',
            name='team',
            field=models.CharField(max_length=40, null=True),
        ),
    ]