# Generated by Django 3.1.7 on 2021-04-07 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210312_2257'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['username']},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='discordid',
            field=models.BigIntegerField(default=9999999999, unique=True),
            preserve_default=False,
        ),
    ]
