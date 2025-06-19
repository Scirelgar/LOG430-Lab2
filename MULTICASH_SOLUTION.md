# Solution Multi-Caisses - Lab 2

## 🎯 Problème Résolu

**Énoncé Lab 1**: "avec 3 caisses qui travaillent simultanément (avoir des transactions pour garantir la consistance)"

**Solution implémentée**: Système de gestion de sessions multi-caisses avec support de 3 terminaux simultanés.

## 🏗️ Architecture de la Solution

### 1. Session Manager (`src/session_manager.py`)
- **CashierSession**: Session simple pour chaque caisse
- **SessionManager**: Gestionnaire thread-safe des sessions multiples
- Isolation des paniers par caisse
- Traçabilité des transactions par caisse

### 2. Controller Modifié (`src/controller/controller.py`)
- Ajout du paramètre `cashier_id` 
- Traçage des ventes par caisse
- Maintien de l'isolation des paniers

### 3. Modèle Sale Étendu (`src/model/sale_model.py`)
- Nouveau champ `cashier_id` pour tracer quelle caisse a effectué la vente
- Migration de base de données automatique

### 4. Application Multi-Terminaux (`src/main_multicash.py`)
- Interface console simplifiée par caisse
- Support des arguments de ligne de commande
- Mode multi-threading pour 3 caisses simultanées
- Mode caisse unique pour conteneurs

## 🚀 Utilisation

### Mode Local - 3 Caisses Simultanées
```bash
cd LOG430-Lab2
python src/main_multicash.py
```

### Mode Caisse Unique
```bash
python src/main_multicash.py --cashier-id 1
python src/main_multicash.py --cashier-id 2
python src/main_multicash.py --cashier-id 3
```

### Mode Docker - 3 Conteneurs
```bash
docker-compose up
```

Chaque caisse aura son propre conteneur :
- `caisse_1` (Caisse 1)
- `caisse_2` (Caisse 2) 
- `caisse_3` (Caisse 3)
- `database` (PostgreSQL partagé)

## 🧪 Tests

```bash
# Tests de la solution multi-caisses
python tests/test_multicash.py

# Tests existants (toujours fonctionnels)
python -m pytest tests/
```

## 📊 Fonctionnalités par Caisse

Chaque caisse peut indépendamment :
- ✅ Ajouter des produits au panier
- ✅ Voir le contenu du panier
- ✅ Finaliser des ventes (avec traçage ID caisse)
- ✅ Lister les produits disponibles
- ✅ Traiter des retours
- ✅ Gestion thread-safe des stocks partagés

## 🔒 Sécurité et Consistance

- **Thread Safety**: Utilisation de `threading.Lock()` dans le SessionManager
- **Isolation des Sessions**: Chaque caisse a son propre contrôleur et panier
- **Transactions DB**: SQLAlchemy gère les transactions ACID sur la base partagée
- **Traçabilité**: Chaque vente est liée à son ID de caisse

## 💡 Avantages de cette Solution

1. **Simplicité**: Réutilise le code existant du Lab 1
2. **Minimal**: Seulement 4 fichiers modifiés/ajoutés
3. **Testable**: Tests unitaires pour valider le comportement
4. **Scalable**: Facile d'ajouter plus de caisses
5. **Docker Ready**: Support conteneurs multiples

## 🔧 Modifications Requises

### Fichiers Modifiés
- `src/controller/controller.py` (ajout cashier_id)
- `src/model/sale_model.py` (champ cashier_id)
- `Dockerfile` (support variable env)
- `compose.yaml` (3 services caisse + database)

### Fichiers Ajoutés
- `src/session_manager.py` (gestion sessions)
- `src/main_multicash.py` (app multi-terminaux)
- `tests/test_multicash.py` (tests validation)

## ✅ Validation Énoncé Lab 1

- [x] Architecture 2-tiers maintenue
- [x] 3 caisses simultanées supportées  
- [x] Transactions pour garantir la consistance
- [x] Gestion des ventes et retours
- [x] Tests automatisés
- [x] Conteneurisation Docker
