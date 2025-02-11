![SoftDesk banner](images/soft-desk-banner.png)

# 📜 API Documentation

This API is documented using Swagger. You can access the interactive documentation at:

- **Swagger UI** : http://127.0.0.1:8000/swagger/
- **ReDoc** : http://127.0.0.1:8000/redoc/

## Project Initialization

1. Clone the project :

```bash
git clone https://github.com/Cyrilebl/soft_desk_API.git
```

2. Create and activate the virtual environment :

```bash
cd soft_desk_API
pipenv shell
```

3. Install dependencies :

```bash
pipenv install
```

4. Run the server :

```bash
cd soft_desk
python manage.py runserver
```

## Endpoints

### 📍 Base URL :

http://127.0.0.1:8000/api/

### 🔑 Authentication : Token

| Method | Endpoint          | Description     |
| ------ | ----------------- | --------------- |
| POST   | `/token/`         | Obtain a token  |
| POST   | `/token/refresh/` | Refresh a token |

### 🟢 Users

| Method      | Endpoint       | Description               | Authentication Required |
| ----------- | -------------- | ------------------------- | :---------------------: |
| POST        | `/users/`      | Create a user             |           ❌            |
| GET         | `/users/`      | Retrieve user information |           ✅            |
| PUT / PATCH | `/users/{id}/` | Update user information   |           ✅            |
| DELETE      | `/users/{id}/` | Delete user account       |           ✅            |

### 🟢 Projects

| Method      | Endpoint          | Description      |       Authorization       |
| ----------- | ----------------- | ---------------- | :-----------------------: |
| POST        | `/projects/`      | Create a project |          _User_           |
| GET         | `/projects/`      | List projects    | _Author_<br>_Contributor_ |
| GET         | `/projects/{id}/` | View a project   | _Author_<br>_Contributor_ |
| PUT / PATCH | `/projects/{id}/` | Update a project |         _Author_          |
| DELETE      | `/projects/{id}/` | Delete a project |         _Author_          |

### 🟢 Contributors

| Method | Endpoint              | Description               |  Authorization   |
| ------ | --------------------- | ------------------------- | :--------------: |
| POST   | `/contributors/`      | Add a contributor         | _Project Author_ |
| GET    | `/contributors/`      | List project contributors | _Project Author_ |
| DELETE | `/contributors/{id}/` | Remove a contributor      | _Project Author_ |

### 🟢 Issues

| Method | Endpoint        | Description         |           Authorization           |
| ------ | --------------- | ------------------- | :-------------------------------: |
| POST   | `/issues/`      | Create an issue     | _Project Author_<br>_Contributor_ |
| GET    | `/issues/`      | List project issues | _Project Author_<br>_Contributor_ |
| GET    | `/issues/{id}/` | View an issue       | _Project Author_<br>_Contributor_ |
| PUT    | `/issues/{id}/` | Update an issue     |             _Author_              |
| DELETE | `/issues/{id}/` | Delete an issue     |             _Author_              |

### 🟢 Comments

| Method | Endpoint          | Description                |           Authorization           |
| ------ | ----------------- | -------------------------- | :-------------------------------: |
| POST   | `/comments/`      | Create a comment           | _Project Author_<br>_Contributor_ |
| GET    | `/comments/`      | List comments for an issue | _Project Author_<br>_Contributor_ |
| GET    | `/comments/{id}/` | View a comment             | _Project Author_<br>_Contributor_ |
| PUT    | `/comments/{id}/` | Update a comment           |             _Author_              |
| DELETE | `/comments/{id}/` | Delete a comment           |             _Author_              |

### _Notes_

- 🔐 _Token authentication is required for all actions._
- 🛠️ _Projects, Issues, and Comments can only be modified by their author._
- 👥 _Only the author or contributors of a project can interact with Issues and Comments._
