from typing import Optional

from pydantic import BaseModel

from database.db import db
from model.channel import RegistrarGerenteZonal


class Zonal(BaseModel):
    id_gerente_zonal: Optional[int] = None
    nombre: str
    email: str
    telefono: str
    cedula: str


async def RegistrarZonal(data: Zonal):
    try:
        print("RegistrarZonal")
        db.execute(
            RegistrarGerenteZonal.insert().values(
                nombre=data.nombre,
                email=data.email,
                telefono=data.telefono,
                cedula=data.cedula,
            )
        )
        return {"status": 200, "message": "Zonal registrada correctamente"}
    except Exception as e:
        print(e)
        return {"status": 400, "message": "Error al registrar la Zonal"}


async def ListarZonalAll():
    try:
        print("ListarZonalAll")
        result = db.execute(RegistrarGerenteZonal.select()).fetchall()
        query = [dict(row._mapping) for row in result]
        return {"status": 200, "data": query}
    except Exception as e:
        print(e)
        return {"status": 400, "message": "Error al listar las Zonal"}


async def ZonalId(id: int):
    try:
        print("ZonalId")
        result = db.execute(
            RegistrarGerenteZonal.select().where(
                RegistrarGerenteZonal.c.id_gerente_zonal == id
            )
        ).fetchall()
        query = [dict(row._mapping) for row in result]
        return query
    except Exception as e:
        print(e)
        return None


async def UpdateZonal(data: Zonal):
    try:
        db.execute(
            RegistrarGerenteZonal.update()
            .where(RegistrarGerenteZonal.c.id_gerente_zonal == data.id_gerente_zonal)
            .values(
                nombre=data.nombre,
                email=data.email,
                telefono=data.telefono,
                cedula=data.cedula,
            )
        )
        return {
            "code": "0",
            "data": "Ciudad actualizada correctamente",
        }
    except Exception as e:
        return {
            "code": "-1",
            "data": "Error: " + str(e),
        }


async def DeleteZonal(id: int):
    try:
        print("DeleteZonal")
        db.execute(
            RegistrarGerenteZonal.delete().where(
                RegistrarGerenteZonal.c.id_gerente_zonal == id
            )
        )
        return {"status": 200, "message": "DeleteZonal correctamente"}
    except Exception as e:
        print(e)
        return {"status": 400, "message": "Error al DeleteZonal"}
