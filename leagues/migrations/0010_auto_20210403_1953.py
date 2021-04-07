# Generated by Django 3.1.7 on 2021-04-03 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0009_left_pick'),
    ]

    operations = [
        migrations.AddField(
            model_name='roster',
            name='deaths',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='roster',
            name='kills',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='draft',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='draft', to='leagues.coach'),
        ),
        migrations.AlterField(
            model_name='roster',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roster', to='leagues.coach'),
        ),
    ]