from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db
from model.administrador import Administradores
from schemas.administrador import Administrador
from datetime import datetime

from starlette.status import HTTP_204_NO_CONTENT


administradores = APIRouter()

@administradores.get("/administradores", tags=["administradores"])
async def get_administradores():
    try:
        query = Administradores.select()
        return db.execute(query).fetchall()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@administradores.get("/administradores/{id}", tags=["administradores"])
async def get_administrador(id: int):
    try:
        return db.execute(Administradores.select().where(Administradores.c.id == id)).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@administradores.post("/administradores", tags=["administradores"])
async def create_administrador(administrador: Administrador):
    new_administrador = {
        "nombreAdministrador": administrador.nombreAdministrador,
        "cedula": administrador.cedula,
        "email": administrador.email,
        "telefono": administrador.telefono,
        "telefono_opt": administrador.telefono_opt,
        "data_creatd": datetime.now(),
    }
    try:
        db.execute(Administradores.insert().values(new_administrador))
        return db.execute(Administradores.select()).fetchall()
    except Exception as e:
        return {"error": str(e.args)}


@administradores.put("/administradores/{id}", tags=["administradores"])
async def update_administrador(id: int, administrador: Administrador):
    try:
        db.execute(
            Administradores.update().values(
                nombreAdministrador=administrador.nombreAdministrador,
                cedula=administrador.cedula,
                email=administrador.email,
                telefono=administrador.telefono,
                telefono_opt=administrador.telefono_opt,
                data_update=datetime.now(),
            ).where(Administradores.c.id == id)
        )
        return db.execute(Administradores.select()).fetchall()
    except Exception as e:
        return {"error": str(e.args)}


@administradores.delete("/administradores/{id}", tags=["administradores"])
async def delete_administrador(id: int):
    try:
        db.execute(Administradores.delete().where(Administradores.c.id == id))
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as e:
        return {"error": str(e.args)}



