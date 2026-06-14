from sqlmodel import SQLModel, Field, create_engine, Session, select
from  typing import Annotated
from fastapi import FastAPI, Depends, Query, HTTPException
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

# CRUD Operations

# Get all heroes
@app.get("/heroes/", response_model=list[HeroPublic])
def get_heroes(
        session: SessionDep, 
        limit: Annotated[int, Query(le=100)] = 5, 
        offset: int = 0
    ):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

# Get hero by id
@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def get_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

# Create a new hero
@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

# Update a hero
@app.put("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

# Delete a hero
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(db_hero)
    session.commit()
    return {"ok": True} 