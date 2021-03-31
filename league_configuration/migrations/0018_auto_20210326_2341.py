# Generated by Django 3.1.7 on 2021-03-26 23:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league_configuration', '0017_season'),
    ]

    operations = [
        migrations.CreateModel(
            name='conference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conference', models.CharField(max_length=40)),
                ('subleague', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league_configuration.subleague')),
            ],
        ),
        migrations.AlterField(
            model_name='season',
            name='draftstart',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='seasonstart',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division', models.CharField(max_length=40)),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league_configuration.conference')),
                ('subleague', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league_configuration.subleague')),
            ],
        ),
    ]
