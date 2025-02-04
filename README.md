![SoftDesk banner](images/soft-desk-banner.png)

# 📌 Endpoints de l'API

## 📍 Base URL :

http://127.0.0.1:8000/api/

## 🔑 Authentification : Token

| Méthode | Endpoint          | Description             |
| ------- | ----------------- | ----------------------- |
| POST    | `/token/`         | Obtenir un token        |
| POST    | `/token/refresh/` | Mettre à jour son token |

### 🟢 Users

| Méthode     | Endpoint       | Description                | Authentification requise |
| ----------- | -------------- | -------------------------- | :----------------------: |
| POST        | `/users/`      | Créer un utilisateur       |            ❌            |
| GET         | `/users/`      | Récupérer ses informations |            ✅            |
| PUT / PATCH | `/users/{id}/` | Modifier ses informations  |            ✅            |
| DELETE      | `/users/{id}/` | Supprimer son compte       |            ✅            |

### 🟢 Projects

| Méthode     | Endpoint          | Description         |        Autorisation        |
| ----------- | ----------------- | ------------------- | :------------------------: |
| POST        | `/projects/`      | Créer un projet     |       _Utilisateur_        |
| GET         | `/projects/`      | Lister les projets  | _Auteur_<br>_Contributeur_ |
| GET         | `/projects/{id}/` | Voir un projet      | _Auteur_<br>_Contributeur_ |
| PUT / PATCH | `/projects/{id}/` | Modifier un projet  |          _Auteur_          |
| DELETE      | `/projects/{id}/` | Supprimer un projet |          _Auteur_          |

### 🟢 Contributors

| Méthode | Endpoint              | Description                          |    Autorisation    |
| ------- | --------------------- | ------------------------------------ | :----------------: |
| POST    | `/contributors/`      | Ajouter un contributeur              | _Auteur du projet_ |
| GET     | `/contributors/`      | Lister les contributeurs d'un projet | _Auteur du projet_ |
| DELETE  | `/contributors/{id}/` | Supprimer un contributeur            | _Auteur du projet_ |

### 🟢 Issues

| Méthode | Endpoint        | Description                   |             Autorisation             |
| ------- | --------------- | ----------------------------- | :----------------------------------: |
| POST    | `/issues/`      | Créer une issue               | _Auteur du projet_<br>_Contributeur_ |
| GET     | `/issues/`      | Lister les issues d'un projet | _Auteur du projet_<br>_Contributeur_ |
| GET     | `/issues/{id}/` | Voir une issue                | _Auteur du projet_<br>_Contributeur_ |
| PUT     | `/issues/{id}/` | Modifier une issue            |               _Auteur_               |
| DELETE  | `/issues/{id}/` | Supprimer une issue           |               _Auteur_               |

### 🟢 Comments

| Méthode | Endpoint          | Description                         |             Autorisation             |
| ------- | ----------------- | ----------------------------------- | :----------------------------------: |
| POST    | `/comments/`      | Créer un commentaire                | _Auteur du projet_<br>_Contributeur_ |
| GET     | `/comments/`      | Lister les commentaires d'une issue | _Auteur du projet_<br>_Contributeur_ |
| GET     | `/comments/{id}/` | Voir un commentaire                 | _Auteur du projet_<br>_Contributeur_ |
| PUT     | `/comments/{id}/` | Modifier un commentaire             |               _Auteur_               |
| DELETE  | `/comments/{id}/` | Supprimer un commentaire            |               _Auteur_               |

## 📌 _Remarques_

- 🔐 _L'authentification Token est requise pour toutes les actions._
- 🛠️ _Les projets, issues et commentaires sont uniquement modifiables par leur auteur._
- 👥 _Seuls l'auteur ou les contributeurs d'un projet peuvent interagir avec les issues et commentaires._
