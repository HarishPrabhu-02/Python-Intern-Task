# Task Manager API - Python Developer Intern Task

A robust, secure backend for a Task Management application built with FastAPI. Features include JWT authentication, user-specific task isolation, and pagination.

## 🚀 Tech Stack
* **Framework:** FastAPI
* **Database:** SQLite & SQLAlchemy (ORM)
* **Validation:** Pydantic
* **Authentication:** JWT (JSON Web Tokens) & Passlib (Bcrypt)

## ⚙️ Local Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/HarishPrabhu-02/Python-Intern-Task](https://github.com/HarishPrabhu-02/Python-Intern-Task)
   cd PythonInternTask
   ```
2. **Set up the virtual environment:**

```Bash
python -m venv .venv
```

**On Mac/Linux:**
```Bash
source .venv/bin/activate  
```

**On Windows:**
```Bash
.venv\Scripts\activate
```

3. **Install Dependencies:**

```Bash
pip install -r requirements.txt
```
4. **Environment Variables:**

Create a .env file in your project root and add:
```Bash
SECRET_KEY=your_generated_secret_key_here
```

Run the Server:
```Bash
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000/docs.

5. **🐳 How to Run with Docker**
If you have Docker installed, you can skip the Python virtual environment setup entirely and spin up the backend with two commands:

```Bash
cd backend
docker build -t task-api .
docker run -p 8000:8000 task-api
```
The API will be available at http://localhost:8000/docs.
