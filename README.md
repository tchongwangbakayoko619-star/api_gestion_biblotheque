# 📚 BiblioAPI

**BiblioAPI** est une API REST de gestion de bibliothèque construite avec Django et Django REST Framework. Elle permet de gérer un catalogue de livres, les emprunts des utilisateurs, et propose une authentification par JWT.

---

## ✨ Fonctionnalités

- 🔐 **Authentification JWT** (via `rest_framework_simplejwt`)
- 👤 **Gestion des utilisateurs** — inscription, profils, rôles (lecteur / bibliothécaire)
- 📖 **Catalogue de livres** — CRUD complet avec suivi des exemplaires disponibles
- 🔄 **Gestion des emprunts** — création, suivi du statut, dates de retour
- 📑 **Documentation API interactive** générée automatiquement avec `drf-spectacular` (Swagger UI)
- ✅ **Suite de tests complète** avec `pytest` et `pytest-django`
- 🧹 **Qualité de code** assurée par `pre-commit` (ruff, djlint, django-upgrade)

---

## 🛠️ Stack technique

| Composant       | Technologie                          |
|-----------------|---------------------------------------|
| Backend         | Django 6.0 / Django REST Framework    |
| Base de données | PostgreSQL                            |
| Auth            | JWT (`djangorestframework-simplejwt`) |
| Documentation   | drf-spectacular (OpenAPI / Swagger)   |
| Gestion de deps | [uv](https://github.com/astral-sh/uv) |
| Tests           | pytest, pytest-django, factory_boy    |
| Qualité de code | ruff, djlint, pre-commit              |

---

## 🚀 Installation

### Prérequis

- Python 3.12+
- PostgreSQL
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Étapes

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com/votre-organisation/biblioapi.git
   cd biblioapi
   ```

2. **Installer les dépendances**

   ```bash
   uv sync
   ```

3. **Configurer les variables d'environnement**

   Copiez le fichier d'exemple et adaptez-le à votre environnement :

   ```bash
   cp .env.example .env
   ```

   Variables clés à renseigner :

   ```env
   DATABASE_URL=postgres://<user>:<password>@127.0.0.1:5432/biblioapi
   POSTGRES_DB=biblioapi
   POSTGRES_USER=<user>
   POSTGRES_PASSWORD=<password>
   ```

4. **Créer la base de données PostgreSQL**

   ```bash
   sudo -u postgres psql -c "CREATE USER <user> WITH PASSWORD '<password>' CREATEDB;"
   sudo -u postgres psql -c "CREATE DATABASE biblioapi OWNER <user>;"
   ```

5. **Appliquer les migrations**

   ```bash
   uv run python manage.py migrate
   ```

6. **Créer un super-utilisateur**

   ```bash
   uv run python manage.py createsuperuser
   ```

7. **Lancer le serveur de développement**

   ```bash
   uv run python manage.py runserver
   ```

   L'API est accessible sur `http://127.0.0.1:8000/`.

---

## 📖 Documentation de l'API

Une fois le serveur lancé, la documentation interactive (Swagger UI) est disponible à :

```
http://127.0.0.1:8000/api/docs/
```

Le schéma OpenAPI brut est disponible à :

```
http://127.0.0.1:8000/api/schema/
```

### Principaux points d'entrée

| Endpoint                | Méthode | Description                          |
|--------------------------|---------|---------------------------------------|
| `/api/inscription/`      | POST    | Créer un compte utilisateur           |
| `/api/token/`            | POST    | Obtenir un token JWT (login)          |
| `/api/token/refresh/`    | POST    | Rafraîchir un token JWT                |
| `/api/moi/`              | GET     | Profil de l'utilisateur connecté       |
| `/api/users/`            | GET     | Liste des utilisateurs                |
| `/api/users/me/`         | GET     | Utilisateur courant (via ViewSet)      |
| `/api/livres/`           | GET/POST| Catalogue de livres                    |
| `/api/emprunts/`         | GET/POST| Gestion des emprunts                   |

---

## 🧪 Lancer les tests

```bash
uv run pytest
```

Avec couverture de code :

```bash
uv run pytest --cov
```

---

## 🧹 Qualité de code

Le projet utilise `pre-commit` pour assurer la cohérence du code avant chaque commit.

**Installation des hooks** (une seule fois) :

```bash
uv run pre-commit install
```

**Lancer manuellement sur tous les fichiers :**

```bash
uv run pre-commit run --all-files
```

---

## 📂 Structure du projet

```
biblioapi/
├── config/                # Configuration Django (settings, urls, routers)
│   ├── settings/
│   └── api_router.py
├── biblioapi/
│   ├── users/              # Gestion des utilisateurs et authentification
│   └── bibliotheque/       # Gestion des livres et emprunts
├── tests/                  # Tests transverses
├── pyproject.toml          # Dépendances et configuration des outils
└── manage.py
```

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! Merci de :

1. Créer une branche depuis `main`
2. Écrire des tests pour toute nouvelle fonctionnalité
3. Vérifier que `pre-commit run --all-files` et `pytest` passent avant de proposer une Pull Request

---

## 📄 Licence

Ce projet est distribué sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.# api_gestion_biblotheque
