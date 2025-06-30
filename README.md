# Flask ToDo MVC WebApp

## Overview

A simple, opinionated ToDo web application built with Flask following the MVC pattern. It provides:

- **User authentication** (register, login, logout) via JWT cookies  
- **User profiles** (email updates)  
- **Hierarchical ToDo items**: Epics, Tasks, Sub-tasks, Bugs  
- **Optional epic relationships** for tasks/bugs; sub-tasks linked to parent tasks  
- **MongoDB** for storage  
- **JSON REST API** documented with Swagger UI  
- **Responsive HTML UI** using Bootstrap 5 and vanilla JS  
- **Docker & Docker Compose** for easy setup

## Features

- **Secure password hashing** with bcrypt  
- **JWT-based sessions** stored in cookies  
- **Role management**: `user` and `admin` (new users default to `user`)  
- **CRUD operations** for ToDo items, including comments and status tracking  
- **Live API docs** at `/api`

## Prerequisites

- **Docker & Docker Compose** (recommended)  
- OR:  
  - Python 3.8+ installed  
  - MongoDB running locally (or update `MONGO_URI`)

## Quickstart with Docker

1. Copy and edit the environment file:  
   ```bash
   cp .env.example .env
   # Update SECRET_KEY, MONGO_URI, etc.
   ```
2. Build and start services:  
   ```bash
   docker-compose up --build -d
   ```
3. Access the app:  
   - **UI**: http://localhost:5000  
   - **Swagger**: http://localhost:5000/api  
4. Stop services:  
   ```bash
   docker-compose down
   ```

## Running Locally Without Docker

Clone the repository and set up:

```bash
git clone <repo-url> flask_todo_mvc
cd flask_todo_mvc

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Adjust SECRET_KEY, MONGO_URI, etc.

# Ensure MongoDB is running (e.g., mongod --dbpath /data/db)

flask run --host=0.0.0.0
```

## Environment Variables

Store secrets in a `.env` file at project root:

```dotenv
SECRET_KEY=your-secret-key
MONGO_URI=mongodb://mongo:27017/tododb
MONGO_HOST=mongo
MONGO_PORT=27017
```

## Project Structure

```
flask_todo_mvc/
├── app.py
├── config.py
├── extensions.py
├── models.py
├── resources/
│   ├── auth.py
│   ├── user.py
│   └── todo.py
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── todos.html
│   ├── todo_detail.html
│   └── epics.html
├── static/
│   └── js/
│       └── main.js
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
└── .env
```

## API Endpoints

**Auth**  
- `POST /api/auth/login` – Authenticate user  

**User**  
- `GET /api/user/` – List users  
- `GET /api/user/profile` – Get current user profile  

**ToDo**  
- `GET /api/todo/` – List all ToDos  
- `POST /api/todo/` – Create a new ToDo  
- `GET /api/todo/{id}` – Get ToDo by ID  
- `PUT /api/todo/{id}` – Update ToDo  
- `DELETE /api/todo/{id}` – Delete ToDo  
- `GET /api/todo/epics` – List all epics  

Browse full Swagger docs at http://localhost:5000/api.

## Contributing

Contributions are welcome! Please:

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/XYZ`)  
3. Commit your changes (`git commit -m "Add XYZ feature"`)  
4. Push to your branch (`git push origin feature/XYZ`)  
5. Open a pull request  

Ensure code follows PEP 8 and includes clear commit messages.