from typing import Optional

from pydantic import BaseModel

from database.db import db
from model.channel import isla


class Isla(BaseModel):
    id: Optional[int] = None
    id_ciudad: int
    isla: str


async def RegistrarIsla(data: Isla):
    try:
        print("RegistrarIsla")
        db.execute(isla.insert().values(id_ciudad=data.id_ciudad, isla=data.isla))
        return {"status": 200, "message": "Isla registrada correctamente"}
    except Exception as e:
        print(e)
        return {"status": 400, "message": "Error al registrar la isla"}


async def ListarIslaAll():
    try:
        print("ListarIslaAll")
        result = db.execute(isla.select()).fetchall()
        query = [dict(row._mapping) for row in result]
        return {"status": 200, "data": query}
    except Exception as e:
        print(e)
        return {"status": 400, "message": "Error al listar las islas"}


async def IslaId(id: int):
    try:
        print("Isla")
        query = db.execute(isla.select().where(isla.c.id == id)).fetchall()
        return query
    except Exception as e:
        print(e)
        return None


async def UpdateIsla(data: Isla):
    try:
        print("UpdateIsla")
        db.execute(
            isla.update()
            .where(isla.c.id == data.id)
            .values(id_ciudad=data.id_ciudad, isla=data.isla)
        )
        return {"status": 200, "message": "Isla actualizada correctamente"}
    except Exception as e:
        print(e)
        return {"status": 400, "message": "Error al actualizar la isla"}


async def DeleteIsla(id: int):
    try:
        print("DeleteIsla")
        db.execute(isla.delete().where(isla.c.id == id))
        return {"status": 200, "message": "Isla eliminada correctamente"}
    except Exception as e:
        print(e)
        return {"status": 400, "message": "Error al eliminar la isla"}
