# FastAPI Blog API

This is a complete backend REST API built with [FastAPI](https://fastapi.tiangolo.com/), designed as an internship project to demonstrate core backend development skills. It features user authentication, database integration, and CRUD operations for blog posts.

## 🚀 Features

- **User Authentication**: Secure user registration and login using JWT (JSON Web Tokens).
- **Password Hashing**: Passwords are securely hashed using bcrypt before being stored in the database.
- **Relational Database**: Uses SQLite and SQLAlchemy ORM with a well-structured `User` and `Post` relationship.
- **Data Validation**: Request and response data is strictly validated and serialized using Pydantic schemas.
- **Pagination**: API endpoints like GET `/api/posts` support `limit` and `skip` parameters for efficient data retrieval.
- **CORS Configured**: Ready to be connected to any frontend framework (React, Vue, etc.).
- **Separation of Concerns**: Clean architecture separating `main.py`, `models.py`, `schemas.py`, `database.py`, and `auth.py`.

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Data Validation**: Pydantic
- **Authentication**: JWT (Jose) & Passlib

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd project-fastapi-blog
   ```

2. **Set up a virtual environment (if not using uv directly):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   # OR if using uv:
   uv sync
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add the following keys (never commit this file to version control):
   ```env
   SECRET_KEY="your-super-secret-key-here"
   DATABASE_URL="sqlite:///./blog.db"
   ```

5. **Run the application:**
   ```bash
   fastapi dev main.py
   ```
   *The server will start at `http://127.0.0.1:8000`.*

## 📚 API Endpoints

Once the server is running, you can view the automatic interactive API documentation at:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Authentication
- `POST /api/register` - Register a new user
- `POST /api/login` - Authenticate user and receive JWT

### Blog Posts
- `POST /api/posts` - Create a new blog post (Requires Auth)
- `GET /api/posts` - Retrieve a list of all posts (Supports pagination: `?limit=10&skip=0`)
- `GET /api/posts/{id}` - Retrieve a specific post by ID
- `PUT /api/posts/{id}` - Update a specific post (Requires Auth, must be author)
- `DELETE /api/posts/{id}` - Delete a specific post (Requires Auth, must be author)
