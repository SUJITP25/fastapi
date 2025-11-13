from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from db.main import init_db

version = "v1"


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Server is Starting...")
    await init_db()
    yield
    print(f"Server has been Stopped")


app = FastAPI(
    title="FastAPI",
    description="A REST API for a my first FASTAPI Application",
    version=version,
    lifespan=life_span,
)


# Practice
# @app.get("/")
# async def home():
#     return {"message": "Welcome to homepage"}


# @app.get("/greet/{name}")
# async def greet(name):
#     return {"message": f"Greeting Message for {name}"}


# class BookCreateModel(BaseModel):
#     title: str
#     author: str


# @app.post("/create-book")
# async def create_book(book_data: BookCreateModel):
#     return {"title": book_data.title, "author": book_data.author}
