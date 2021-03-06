# Generated by Django 3.1.7 on 2021-03-12 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='move',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('move_typing', models.CharField(max_length=10)),
                ('move_category', models.CharField(max_length=10)),
                ('move_power', models.IntegerField()),
                ('move_accuracy', models.IntegerField()),
                ('move_priority', models.IntegerField()),
                ('move_crit_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('secondary_effect_chance', models.IntegerField()),
                ('secondary_effect', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='pokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('pokedex_number', models.IntegerField(default=0)),
                ('sprite', models.URLField(default='https://claduva.github.io/pdl_images/sprites/default.png')),
                ('data', models.JSONField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='pokemon_effectiveness',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bug', models.IntegerField(default=0)),
                ('dark', models.IntegerField(default=0)),
                ('dragon', models.IntegerField(default=0)),
                ('electric', models.IntegerField(default=0)),
                ('fairy', models.IntegerField(default=0)),
                ('fighting', models.IntegerField(default=0)),
                ('fire', models.IntegerField(default=0)),
                ('flying', models.IntegerField(default=0)),
                ('ghost', models.IntegerField(default=0)),
                ('grass', models.IntegerField(default=0)),
                ('ground', models.IntegerField(default=0)),
                ('ice', models.IntegerField(default=0)),
                ('normal', models.IntegerField(default=0)),
                ('poison', models.IntegerField(default=0)),
                ('psychic', models.IntegerField(default=0)),
                ('rock', models.IntegerField(default=0)),
                ('steel', models.IntegerField(default=0)),
                ('water', models.IntegerField(default=0)),
                ('pokemon', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='effectiveness', to='pokemon.pokemon')),
            ],
        ),
        migrations.CreateModel(
            name='pokemon_battlestats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kills', models.IntegerField(default=0)),
                ('deaths', models.IntegerField(default=0)),
                ('differential', models.IntegerField(default=0)),
                ('gp', models.IntegerField(default=0)),
                ('gw', models.IntegerField(default=0)),
                ('support', models.IntegerField(default=0)),
                ('damagedone', models.IntegerField(default=0)),
                ('hphealed', models.IntegerField(default=0)),
                ('luck', models.FloatField(default=0)),
                ('remaininghealth', models.IntegerField(default=0)),
                ('pokemon', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='battlestats', to='pokemon.pokemon')),
            ],
        ),
        migrations.CreateModel(
            name='pokemon_basestats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hp', models.IntegerField(default=0)),
                ('attack', models.IntegerField(default=0)),
                ('defense', models.IntegerField(default=0)),
                ('special_attack', models.IntegerField(default=0)),
                ('special_defense', models.IntegerField(default=0)),
                ('speed', models.IntegerField(default=0)),
                ('bst', models.IntegerField(default=0)),
                ('pokemon', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='basestats', to='pokemon.pokemon')),
            ],
        ),
        migrations.CreateModel(
            name='pokemon_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=15)),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types', to='pokemon.pokemon')),
            ],
            options={
                'unique_together': {('pokemon', 'type')},
            },
        ),
        migrations.CreateModel(
            name='pokemon_moveset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('move', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemon.move')),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moveset', to='pokemon.pokemon')),
            ],
            options={
                'ordering': ['move__name'],
                'unique_together': {('pokemon', 'move')},
            },
        ),
        migrations.CreateModel(
            name='pokemon_ability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ability', models.CharField(max_length=30)),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abilities', to='pokemon.pokemon')),
            ],
            options={
                'unique_together': {('pokemon', 'ability')},
            },
        ),
    ]
