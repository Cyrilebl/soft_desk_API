![LITRevu banner](images/soft-desk-banner.png)

# 📌 Endpoints de l'API

## 📍 Base URL :

http://127.0.0.1:8000/api/

## 🔑 Authentification : Token (via Authorization: Token VOTRE_TOKEN)

### 🟢 Users

| Méthode | Endpoint       | Description                | Authentification requise |
| ------- | -------------- | -------------------------- | :----------------------: |
| GET     | `/users/`      | Récupérer ses informations |            ✅            |
| POST    | `/users/`      | Créer un utilisateur       |            ❌            |
| PUT     | `/users/{id}/` | Modifier ses informations  |            ✅            |
| DELETE  | `/users/{id}/` | Supprimer son compte       |            ✅            |

### 🟢 Projects

| Méthode | Endpoint          | Description                | Authentification requise |
| ------- | ----------------- | -------------------------- | :----------------------: |
| GET     | `/projects/`      | Lister les projets         |    ✅ <br> _(Auteur)_    |
| GET     | `/projects/{id}/` | Récupérer un projet par ID |    ✅ <br> _(Auteur)_    |
| POST    | `/projects/`      | Créer un projet            |    ✅ <br> _(Auteur)_    |
| PUT     | `/projects/{id}/` | Modifier un projet         |    ✅ <br> _(Auteur)_    |
| DELETE  | `/projects/{id}/` | Supprimer un projet        |    ✅ <br> _(Auteur)_    |

### 🟢 Contributors

| Méthode | Endpoint              | Description                          |   Authentification requise   |
| ------- | --------------------- | ------------------------------------ | :--------------------------: |
| GET     | `/contributors/`      | Lister les contributeurs d'un projet | ✅ <br> _(Auteur du projet)_ |
| POST    | `/contributors/`      | Ajouter un contributeur              | ✅ <br> _(Auteur du projet)_ |
| DELETE  | `/contributors/{id}/` | Supprimer un contributeur            | ✅ <br> _(Auteur du projet)_ |

### 🟢 Issues

| Méthode | Endpoint        | Description                    | Authentification requise |
| ------- | --------------- | ------------------------------ | :----------------------: |
| GET     | `/issues/`      | Lister les issues d'un projet  | ✅ <br> _(Contributeur)_ |
| GET     | `/issues/{id}/` | Récupérer une issue spécifique | ✅ <br> _(Contributeur)_ |
| POST    | `/issues/`      | Créer une issue                | ✅ <br> _(Contributeur)_ |
| PUT     | `/issues/{id}/` | Modifier une issue             |    ✅ <br> _(Auteur)_    |
| DELETE  | `/issues/{id}/` | Supprimer une issue            |    ✅ <br> _(Auteur)_    |

### 🟢 Comments

| Méthode | Endpoint          | Description                         | Authentification requise |
| ------- | ----------------- | ----------------------------------- | :----------------------: |
| GET     | `/comments/`      | Lister les commentaires d'une issue | ✅ <br> _(Contributeur)_ |
| GET     | `/comments/{id}/` | Récupérer un commentaire            | ✅ <br> _(Contributeur)_ |
| POST    | `/comments/`      | Ajouter un commentaire              | ✅ <br> _(Contributeur)_ |
| PUT     | `/comments/{id}/` | Modifier un commentaire             |    ✅ <br> _(Auteur)_    |
| DELETE  | `/comments/{id}/` | Supprimer un commentaire            |    ✅ <br> _(Auteur)_    |

```markdown
📌 Remarques

- 🔐 L'authentification Token est requise pour toutes les actions sauf la création d'un utilisateur.
- 👥 Un utilisateur ne peut voir/modifier que ses propres informations.
- 🏗️ Les projets sont gérés uniquement par leur créateur (ajout/modif/suppression).
- 🛠️ Les issues et commentaires sont modifiables uniquement par leur auteur.
- 👥 Seul les contributeurs d'un projet peuvent interagir avec les issues et commentaires.
```
