from http.client import HTTPException
from multiprocessing import synchronize
from time import time
from turtle import update
from typing import Optional, List
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from requests import Session, post, session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# connecting to the database
# if condition of the connection true, connected. if false, it throws error, connecting failed. 
while True:  
    try:
        conn = psycopg2.connect(host= 'localhost' , database='fastapi', user='postgres', password='a742141189', cursor_factory=RealDictCursor) # connecting to postgres local db
        cursor = conn.cursor() # variable cursor to database
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("connecting failed")
        print("Error: ", error)
        time.sleep(3)

#this is no longer used
my_post = [{"title" : "title of post 1", "content": "content of post 1", "id": 1}, {"title": "fav food", "content": "i like pisha", "id" : 2}]

# find posts using id
def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p

# finding an index for every post existing with id as requirements
def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i

# taking the router into main file
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)



 # ================================================================================================================== #

