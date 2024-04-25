from fastapi import FastAPI, Depends, Path, HTTPException
from pydantic import BaseModel
from database import engineconn
from models import Test

app = FastAPI()

engine = engineconn()
session_maker = engine.sessionmaker()


class Item(BaseModel):
    name : str
    number : int

@app.get("/")
async def first_get():
    example = session_maker.query(Test).all()
    return example
