''' This is the main point of execution for our API'''
from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos, admin, users

# Create a new instance of a FastAPI Application
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Add routers to our resources to our app.
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
