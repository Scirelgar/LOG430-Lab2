# Décision d'architecture - Choix de la base de données

Titre : PostgreSQL comme base de données relationnelle

## Contexte

Dans le cadre du projet LOG430, une base de données relationnelle est nécessaire pour stocker les données de l'application. Le choix de la base de données doit prendre en compte la scalabilité, la performance, la résilience et la compatibilité avec les outils et technologies utilisés. Le choix s'est porté entre PostgreSQL et MySQL, deux bases de données relationnelles populaires et ouvertes. PostgreSQL est cependant plus estimé pour flexibilité et ses performances à grande échelle, tandis que MySQL est souvent préféré pour sa simplicité et sa facilité d'implémentation.

## Décision

PostgreSQL sera utilisée comme base de données relationnelle.

## Justification

1. **Performance et scalabilité** : PostgreSQL est reconnu pour sa capacité à gérer de grandes quantités de données et à offrir de bonnes performances, même avec des requêtes complexes.
2. **Support et communauté** : PostgreSQL dispose d'une large communauté et d'un support actif, ce qui facilite la résolution de problèmes et l'accès à des ressources.
3. **Propriétés ACID** : PostgreSQL garantit les propriétés ACID (Atomicité, Cohérence, Isolation, Durabilité), essentielles pour les applications nécessitant une intégrité des données.
4. **Contrôle des transactions concurrentes** : PostgreSQL offre des mécanismes avancés de contrôle des transactions concurrentes, ce qui est crucial pour les applications à fort trafic.
5. **Support des types de données** : PostgreSQL est dit *object-relational*, ce qui signifie que des objets complexes peuvent être stockés et manipulés directement dans la base de données, offrant une flexibilité supplémentaire pour les modèles de données.

## Alternatives considérées

MySQL a été considéré comme une alternative, mais il a été écarté en raison d'un degré de maturité et de fonctionnalités moins avancées par rapport à PostgreSQL, sur la plupart des critères mentionnés ci-dessus. Bien que MySQL soit plus simple à mettre en place, PostgreSQL offre une meilleure flexibilité et des performances supérieures pour les applications à grande échelle. MySQL semble plus léger en plus d'être écrit en C et C++, il est donc très rapide et performant, particulièrement en lecture. Comme un système de caisse enregistre des transactions, la performance en écriture semble plus importante que la performance en lecture.

## Conclusion

Le choix de PostgreSQL comme base de données relationnelle est justifié par ses performances, sa scalabilité, son support des transactions ACID et sa flexibilité. Ce choix permettra de répondre efficacement aux besoins actuels du projet tout en préparant le terrain pour une évolution future de l'application.

## Liens

- [PostgreSQL Documentation](https://www.postgresql.org/about/)
- [MySQL Documentation](https://dev.mysql.com/doc/refman/8.4/en/features.html)
- [What’s the Difference Between MySQL and PostgreSQL?](https://aws.amazon.com/compare/the-difference-between-mysql-vs-postgresql/)
