# Choix des technologies

Langage: Python
ORM : SQLAlchemy
Database : PostgreSQL

## Langage : Python

### Avantages

Pour des besoins de prototypage, python est le langage tout désigné. C'est aussi un langage bien maîtrisé et disposant d'une très vaste collection de cadriciel de développement pour divers applications backend.

### Limitations

Les limitations à considérer dans le cadre de laboratoires d'architecture est principalement le plafond de performance, notamment le manque de support pour du multi-threading.

Il est possible d'émuler du multi-threading avec divers librairies Python et il est possible également d'utiliser la fonctionnalité expérimentale de multi-threading en Python 3.13.

## Object Relational Mapper : SQL Alchemy ou SQL Model

SQL Alchemy est généralement assez répandu en Python. Cependant, comme l'application sera éventuellement portée à du Web, et que la technologie FastAPI risque d'être utilisée, c'est plutôt un ORM basé sur SQL Alchemy qui devrait être utilisé appelé [SQL Model](https://fastapi.tiangolo.com/tutorial/sql-databases/)

## Database : PostgreSQL

La base de donnée PostgreSQL est open source en plus d'être supportée par l'ORM SQLAlchemy
