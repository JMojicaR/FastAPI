from pydantic import BaseModel, Field
from fastapi import FastAPI, Query, HTTPException
from typing import Annotated, Literal
from itertools import count

next_id = count(start=1)  # Empezamos desde 6 porque ya tenemos 5 tareas en la base de datos falsa

def get_next_id():
    return next(next_id)

class TareaBase(BaseModel):
    titulo: Annotated[str, Field(min_length=3)]
    estado: Literal['pendiente', 'completada'] = 'pendiente'

class TareaCreate(TareaBase):
    pass

class TareaFullUpdate(BaseModel):
    titulo: Annotated[str, Field(min_length=3)]
    estado: Literal['pendiente', 'completada']

class TareaPartialUpdate(BaseModel):
    titulo: Annotated[str | None, Field(min_length=3)] = None
    estado: Literal['pendiente', 'completada'] | None = None

class Tarea(TareaBase):
    id: Annotated[int, Field(gt=0)]

class FilterParams(BaseModel):
    limit: Annotated[int, Field(gt=1)] = 5
    offset: Annotated[int, Field(ge=0)] = 0
    estado: Literal['pendiente', 'completada'] | None = None
    search: str | None = None

fake_db: list[Tarea] = [
    Tarea(id=get_next_id(), titulo="Comprar leche", estado="pendiente"),
    Tarea(id=get_next_id(), titulo="Hacer ejercicio", estado="completada"),
    Tarea(id=get_next_id(), titulo="Leer un libro", estado="pendiente"),
    Tarea(id=get_next_id(), titulo="Escribir código", estado="completada"),
    Tarea(id=get_next_id(), titulo="Lavar el coche", estado="pendiente")
]

app = FastAPI()

@app.get("/tareas/", response_model=list[Tarea])
async def get_tareas(filter_query: Annotated[FilterParams, Query()]):
    # filtered_tasks = ([tarea for tarea in fake_db if tarea.estado == filter_query.estado] if filter_query.estado else fake_db)
    # [filter_query.offset: filter_query.offset + filter_query.limit]
    if filter_query.estado:
        filtered_tasks = [tarea for tarea in fake_db if tarea.estado == filter_query.estado]
    else:
        filtered_tasks = fake_db

    # Filtrado con search
    if filter_query.search:
        filtered_tasks = [tarea for tarea in filtered_tasks if filter_query.search.lower() in tarea.titulo.lower()]
    return filtered_tasks[filter_query.offset: filter_query.offset + filter_query.limit]
        #return fake_db[filter_query.offset: filter_query.offset + filter_query.limit]
        #return fake_db

@app.get("/tareas/{tarea_id}", response_model=Tarea)
async def get_tarea(tarea_id: int):
    tarea = next((tarea for tarea in fake_db if tarea.id == tarea_id), None)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

@app.post("/tareas/", response_model=Tarea, status_code=201)
async def create_tarea(tarea: TareaCreate):
    nuevo_id: int = get_next_id()
    nueva_task: Tarea = Tarea(id=nuevo_id, **tarea.model_dump())
    fake_db.append(nueva_task)
    return nueva_task

@app.put("/tareas/{tarea_id}", response_model=Tarea)
async def update_tarea(tarea_id: int, tarea: TareaFullUpdate):
    tarea_index = next((index for index, t in enumerate(fake_db) if t.id == tarea_id), None)
    if tarea_index is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    tarea_actual = fake_db[tarea_index]
    updated_task = tarea_actual.model_copy(update=tarea.model_dump())
    fake_db[tarea_index] = updated_task
    return updated_task

@app.patch("/tareas/{tarea_id}", response_model=Tarea)
async def update_tarea_partial(tarea_id: int, tarea: TareaPartialUpdate):
    tarea_index = next((index for index, t in enumerate(fake_db) if t.id == tarea_id), None)
    if tarea_index is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    if tarea.titulo is None and tarea.estado is None:
        raise HTTPException(status_code=400, detail="Al menos un campo debe ser proporcionado para la actualización")
    if tarea.titulo is not None and tarea.estado is not None:
        raise HTTPException(status_code=400, detail="Solo debe proporcionar un campo para la actualización parcial")
    tarea_actual = fake_db[tarea_index]
    updated_task = tarea_actual.model_copy(update=tarea.model_dump(exclude_unset=True))
    fake_db[tarea_index] = updated_task
    return updated_task

@app.delete("/tareas/{tarea_id}", status_code=204)
async def delete_tarea(tarea_id: int):
    tarea_index = next((index for index, t in enumerate(fake_db) if t.id == tarea_id), None)
    if tarea_index is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    del fake_db[tarea_index]
    return None