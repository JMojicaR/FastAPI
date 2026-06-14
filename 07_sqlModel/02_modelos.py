from sqlmodel import SQLModel, Field, create_engine, Session
from  typing import Annotated
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

# Modelo base
class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)

# Modelo base de datos
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str

# Modelo publico
class HeroPublic(HeroBase):
    id: int

# Modelo de creación
class HeroCreate(HeroBase):
    secret_name: str

# Modelo para update
class HeroUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None

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