from fastapi import FastAPI, Body, Query, HTTPException

# Serves as the foundation for our application: https://docs.sqlalchemy.org/en/20/core/engines.html
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Ideally, a connection string as a variable.
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

# Create an instance of a connection to the database at our database URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# a Session for connecting to and interacting with our database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Allows us to create database tables.
Base = declarative_base()
