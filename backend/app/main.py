from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import auth_router, task_router

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="Backend for the Python Developer Intern Task",
    version="1.0.0"
)

# Configure CORS so your frontend can communicate with your backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your routers
app.include_router(auth_router.router)
app.include_router(task_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Task Manager API! Visit /docs to see the Swagger UI."}