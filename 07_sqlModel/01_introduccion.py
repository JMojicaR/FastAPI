from sqlmodel import SQLModel, Field, create_engine, Session
from  typing import Annotated
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


sqlite_file_name = "heroes.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# Lifespan Events

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to be execcuted before the application starts
    create_db_and_tables()
    yield
    # Code to be execcuted after the application stops

app = FastAPI(lifespan=lifespan)