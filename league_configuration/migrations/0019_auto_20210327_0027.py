# Generated by Django 3.1.7 on 2021-03-27 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league_configuration', '0018_auto_20210326_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='subleague',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conferences', to='league_configuration.subleague'),
        ),
        migrations.AlterField(
            model_name='division',
            name='conference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conference_divisions', to='league_configuration.conference'),
        ),
        migrations.AlterField(
            model_name='division',
            name='subleague',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='divisions', to='league_configuration.subleague'),
        ),
    ]