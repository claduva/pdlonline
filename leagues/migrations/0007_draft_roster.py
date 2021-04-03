# Generated by Django 3.1.7 on 2021-04-02 04:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0001_initial'),
        ('leagues', '0006_coach'),
    ]

    operations = [
        migrations.CreateModel(
            name='roster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wins', models.IntegerField(default=0)),
                ('losses', models.IntegerField(default=0)),
                ('differential', models.IntegerField(default=0)),
                ('streak', models.IntegerField(default=0)),
                ('support', models.IntegerField(default=0)),
                ('damagedone', models.IntegerField(default=0)),
                ('hphealed', models.IntegerField(default=0)),
                ('luck', models.FloatField(default=0)),
                ('remaininghealth', models.IntegerField(default=0)),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemon.pokemon')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.coach')),
            ],
        ),
        migrations.CreateModel(
            name='draft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picknumber', models.IntegerField()),
                ('picktime', models.DateTimeField(auto_now=True, null=True)),
                ('skipped', models.BooleanField(default=False)),
                ('announced', models.BooleanField(default=False)),
                ('pokemon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pokemon.pokemon')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.coach')),
            ],
        ),
    ]
