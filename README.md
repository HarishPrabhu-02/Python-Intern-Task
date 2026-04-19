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

6. **Deployment Link:https://python-intern-task.onrender.com/docs**

7. **How to Test in Swagger UI (/docs):**

Since this API is secured with JWT Authentication, you must create a user and log in before you can manage tasks. 

1. **Navigate to the Docs:** Open your live URL (e.g., `https://python-intern-task.onrender.com/docs`).
2. **Register a User:**
   * Scroll to the **`POST /auth/register`** endpoint and click it.
   * Click the **"Try it out"** button.
   * Change the JSON body to include a username and password:
     ```json
     {
       "username": "testuser",
       "password": "mysecurepassword"
     }
     ```
   * Click **Execute**. You should see a `201 Created` response.
3. **Authorize (Log in):**
   * Scroll to the very top of the page and click the green **Authorize** button (padlock icon).
   * Enter the exact `username` and `password` you just created. *(Leave client_id and client_secret blank).*
   * Click **Authorize**, then click **Close**.
4. **Test Protected Routes:**
   * Swagger UI will now automatically attach your secure JWT token to all future requests! 
   * Try going to **`POST /tasks/`**, clicking "Try it out", and executing a request to create your first task.
