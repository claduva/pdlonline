# Generated by Django 3.1.7 on 2021-04-16 01:14

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draft_planner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draft_plan',
            name='associatedleague',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='draft_plan',
            name='team',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), null=True, size=None),
        ),
    ]
