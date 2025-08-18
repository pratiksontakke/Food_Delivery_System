from fastapi import FastAPI
from pydantic import BaseModel

from api.db.database import Base


app = FastAPI()

class Post(Base):
    id: 

class Post(BaseModel):

