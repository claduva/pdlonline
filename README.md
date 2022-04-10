

<div align="center">
	<img height="200" src="main/static/images/pdllogo.png" alt="Pokemon Draft League">
</div>

<br>

A Pokemon Draft League platform: [pokemondraftleague.online](https://pokemondraftleague.online/)

Running
========================================

You can run this locally simply using the docker-compose file:

```
docker-compose up
```

Then create a superuser using:

```
docker-compose exec backend python manage.py createsuperuser
```


And then populate the database with pokemon data

```
docker-compose exec backend python manage.py import_pokemons
```

You can then access the website using `localhost:8000`