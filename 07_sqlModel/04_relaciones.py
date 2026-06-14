from sqlmodel import SQLModel, Field, create_engine, Session, select, Relationship
from  typing import Annotated
from fastapi import FastAPI, Depends, Query, HTTPException
from contextlib import asynccontextmanager

# Modelo base
class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)

class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str


# Modelo base de datos

class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    heroes: list["Hero"] = Relationship(back_populates="team")

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str
    team_id: int | None = Field(default=None, foreign_key="team.id")
    team: Team | None = Relationship(back_populates="heroes")


# Modelo publico
class HeroPublic(HeroBase):
    id: int
    team: Team | None = None

class TeamPublic(TeamBase):
    id: int
    heroes: list[Hero] = []

# Modelo de creación

class TeamCreate(TeamBase):
    pass

class HeroCreate(HeroBase):
    team_id: int | None = None
    secret_name: str

# Modelo para update

class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None

class HeroUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
    team_id: int | None = None


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

# Teams

# Get all teams
@app.get("/teams/", response_model=list[TeamPublic])
def get_teams(session: SessionDep):
    teams = session.exec(select(Team)).all()
    return teams

# Get team by id
@app.get("/teams/{team_id}", response_model=TeamPublic)
def get_team(team_id: int, session: SessionDep):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

# Create a new team
@app.post("/teams/", response_model=TeamPublic)
def create_team(team: TeamCreate, session: SessionDep):
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

# Update a team 
@app.put("/teams/{team_id}", response_model=TeamPublic)
def update_team(team_id: int, team: TeamUpdate, session: SessionDep):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.model_dump(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

# Delete a team
@app.delete("/teams/{team_id}")
def delete_team(team_id: int, session: SessionDep):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    #opcion1
    for hero in db_team.heroes:
        hero.team = None
    #opcion2
    # for hero in db_team.heroes:
    #     session.delete(hero)
    session.delete(db_team)
    session.commit()
    return {"ok": True}