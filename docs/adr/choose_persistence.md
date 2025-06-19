# Décision d'architecture - Choix de la persistance

Titre : Repository comme patron de conception pour la persistance

## Contexte

Dans le cadre du projet LOG430, bien qu'une architecture de petite envergure soit implémentée au départ, celle-ci tendra à évoluer vers une architecture plus complexe avec des requis de mise à l'échelle importants. Celle-ci sera également mise à l'épreuve par des tests de résilience et de performance. Après lecture des documents de référence et des patrons de conception, les options étaient réduites aux patrons Repository et Data Mapper pour la persistance des données. Le patron Repository est choisi pour sa simplicité et sa flexibilité, tandis que le patron Data Mapper est écarté en raison de la complexité inutile qu'il introduirait dans le contexte actuel du projet.

## Décision

Le patron Repository sera utilisé pour la persistance des données.

## Justification

1. **Abstraction de la persistance** : Le patron Repository permet d'abstraire les détails de la persistance des données, facilitant ainsi les modifications futures sans impacter le reste de l'application.
2. **Simplicité** : Le patron Repository est simple à implémenter et à comprendre, surtout pour une petite application. En effet, étant donné le contexte du projet et les ressources à disposition, le patron Repository seul suffit pour répondre aux besoins de persistance.
3. **Flexibilité** : Le patron Repository permet de changer facilement la source de données (par exemple, passer d'une base de données relationnelle à une base de données NoSQL) sans modifier le code métier.
4. **Tests unitaires** : Le patron Repository facilite les tests unitaires en permettant de simuler la couche de persistance, ce qui est essentiel pour assurer la qualité du code dans un projet évolutif.

## Alternatives considérées

Le patron Data Mapper, bien que considéré, a été écarté. Comme SQLAlchemy est un des outils sélectionnés, celui-ci peut-être utilisé en mode Core ou ORM, le dernier étant plus adapté pour le patron Repository et permettant de se passer de la couche Data Mapper. En d'autres termes, utiliser SQLAlchemy en mode ORM avec le patron Data Mapper serait redondant et inutilement complexe pour les besoins actuels du projet.

## Conclusion

Le choix du patron Repository pour la persistance des données est justifié par sa simplicité, sa flexibilité et sa capacité à s'adapter à l'évolution de l'architecture du projet. Ce choix permettra de répondre efficacement aux besoins actuels tout en préparant le terrain pour une évolution future de l'application.

## Liens

- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [Data Mapper Pattern](https://martinfowler.com/eaaCatalog/dataMapper.html)
- [SQLAlchemy Core Documentation](https://docs.sqlalchemy.org/en/20/core/)
- [SQLAlchemy ORM Documentation](https://docs.sqlalchemy.org/en/20/orm/)
