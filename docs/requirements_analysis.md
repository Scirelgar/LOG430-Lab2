# Analyse des besoins

## Besoins fonctionnels

- L'utilisateur doit pouvoir démarrer l'application avec docker.
- L'utilisateur doit interagir avec un système de caisse simple sour la forme d'une application console ou une application de bureau.
- L'utilisateur doit pouvoir rechercher un produit par identifiant, nom ou catégorie.
- L'utilisateur doit pouvoir consulter l'inventaire de produits ou l'état du stock (disponible ou non).
- L'utilisateur doit pouvoir enregistrer une vente en sélectionnant un produit et en indiquant la quantité.
- L'utilisateur doit pouvoir gérer un retour de produit en annulant une vente.

## Besoins non fonctionnels

- L'application doit être conteneurisée avec Docker.
- L'application doit être testée avec des tests unitaires.
- L'application est séparée en deux couches : une couche client et une couche serveur.
- Dans le case de ce laboratoire, la couche serveur n'est qu'une base de données locale.
- Le client doit interagir avec la base de données à l'aide d'un ORM.
