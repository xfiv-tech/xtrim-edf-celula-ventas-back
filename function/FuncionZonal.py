

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


async def RegistrarZonal(data:Zonal):
    try:
        print("RegistrarZonal")
        db.execute(RegistrarGerenteZonal.insert().values(
            nombre = data.nombre,
            email = data.email,
            telefono = data.telefono,
            cedula = data.cedula
        ))
        return {
            "status": 200,
            "message": "Zonal registrada correctamente"
        }
    except Exception as e:
        print(e)
        return {
            "status":400,
            "message": "Error al registrar la Zonal"
        }
    
    
async def ListarZonalAll():
    try:
        print("ListarZonalAll")
        query = db.execute(RegistrarGerenteZonal.select()).fetchall()
        return {
            "status": 200,
            "data": query
        }
    except Exception as e:
        print(e)
        return {
            "status":400,
            "message": "Error al listar las Zonal"
        }
    
async def ZonalId(id:int):
    try:
        print("ZonalId")
        query = db.execute(RegistrarGerenteZonal.select().where(RegistrarGerenteZonal.c.id_gerente_zonal == id)).fetchall()
        return query
    except Exception as e:
        print(e)
        return None

    
async def UpdateZonal(data:Zonal):
    try:
        print("UpdateZonal")
        db.execute(RegistrarGerenteZonal.update().where(RegistrarGerenteZonal.c.id_gerente_regional == data.id).values(
            nombre = data.nombre,
            email = data.email,
            telefono = data.telefono,
            cedula = data.cedula,
        ))
        return {
            "status": 200,
            "message": "UpdateZonal correctamente"
        }
    except Exception as e:
        print(e)
        return {
            "status":400,
            "message": "Error la UpdateZonal"
        }
        
async def DeleteZonal(id:int):
    try:
        print("DeleteZonal")
        db.execute(RegistrarGerenteZonal.delete().where(RegistrarGerenteZonal.c.id_gerente_zonal == id))
        return {
            "status": 200,
            "message": "DeleteZonal correctamente"
        }
    except Exception as e:
        print(e)
        return {
            "status":400,
            "message": "Error al DeleteZonal"
        }