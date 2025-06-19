# LOG430-Lab1

## Description

TODO

## Installation et exécution

### Local

TODO

### Docker

Le projet contient un ficher `compose.yaml` qui permet de lancer l'application dans un conteneur Docker. Pour ce faire, il ne suffit que de lancer la commande suivante :

```bash
docker compose up
```

Cela va construire l'image Docker et démarrer le conteneur.

## Structure du projet

```
src
└── pkg
    ├── __init__.py
    └── main.py
tests
├── __init__.py
└── test_main.py
README.md
requirements.txt
```

### src

Le module `src` contient le code source de l'application.

### tests

Le module `tests` contient les tests unitaires pour l'application.

## CI/CD

Le projet utilise des GitHub Actions pour la CI/CD. Trois workflows sont configurés :

| Workflow | Description | Triggers |
| --- | --- | --- |
| `black_formatting.yml` | Vérifie le formatage du code avec Black | `push`, `pull_request` |
| `docker_publish.yml` | Construit l'image Docker et la pousse sur Docker Hub | `push` sur la branche `master` |
| `unit_test.yml` | Exécute les tests unitaires | `pull_request` |
