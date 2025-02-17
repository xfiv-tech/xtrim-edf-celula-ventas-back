from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db
from model.administrador import Administradores
from model.edificio import Edicifios
from schemas.administrador import Administrador
from schemas.adminstradorList import AdministradorList
from schemas.adminCedula import AdminCedula
from datetime import datetime
from middleware.validacionToken import ValidacionToken

from starlette.status import HTTP_204_NO_CONTENT


administradores = APIRouter(route_class=ValidacionToken)


@administradores.post("/administradores", tags=["administradores"])
async def get_administradores():
    try:
        result = db.execute(Administradores.select()).fetchall()
        db.commit()
        data = [dict(row._mapping) for row in result]
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@administradores.post("/administradores_id", tags=["administradores"])
async def get_administrador(adminID: AdministradorList):
    try:
        data = db.execute(
            Administradores.select().where(Administradores.c.id == adminID.id)
        ).first()
        db.commit()
        return {
            "code": "0",
            "data": data,
            "message": "Administrador listado correctamente",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@administradores.post("/administradores_crear", tags=["administradores"])
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
        data = db.execute(Administradores.select()).fetchall()
        db.commit()
        return {
            "code": "0",
            "data": data,
            "message": "Administrador creado correctamente",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@administradores.put("/administradores_actualizar", tags=["administradores"])
async def update_administrador(administrador: Administrador):
    try:
        db.execute(
            Administradores.update()
            .values(
                nombreAdministrador=administrador.nombreAdministrador,
                cedula=administrador.cedula,
                email=administrador.email,
                telefono=administrador.telefono,
                telefono_opt=administrador.telefono_opt,
                data_update=datetime.now(),
            )
            .where(Administradores.c.id == administrador.id)
        )
        data = db.execute(Administradores.select()).fetchall()
        db.commit()
        return {
            "code": "0",
            "data": data,
            "message": "Administrador actualizado correctamente",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@administradores.delete("/administradores", tags=["administradores"])
async def delete_administrador(adminID: AdministradorList):
    try:
        db.execute(Administradores.delete().where(Administradores.c.id == adminID.id))
        db.commit()
        return {
            "code": "0",
            "data": [],
            "message": "Administrador eliminado correctamente",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@administradores.post("/administradores_cedula", tags=["administradores"])
async def get_administrador_cedula(admCedula: AdminCedula):
    try:
        data = db.execute(
            Administradores.select().where(Administradores.c.cedula == admCedula.cedula)
        ).first()
        dataE = db.execute(
            Edicifios.select().where(Edicifios.c.idAdministrador == data.id)
        ).fetchall()
        edificios = []
        for i in dataE:
            edificios.append(
                {
                    "id_usuario": i.id_usuario,
                    "idAdministrador": i.idAdministrador,
                    "id_edificio": i.id_edificio,
                    "sector": i.sector,
                    "ciudad": i.ciudad,
                    "coordenadas": i.coordenadas,
                    "ctaReferencia": i.ctaReferencia,
                    "cedulaReferencia": i.cedulaReferencia,
                    "nombreEdificio": i.nombreEdificio,
                    "referencia": i.referencia,
                    "responsable": i.responsable,
                }
            )

        info = {
            "id": data.id,
            "nombreAdministrador": data.nombreAdministrador,
            "cedula": data.cedula,
            "email": data.email,
            "telefono": data.telefono,
            "telefono_opt": data.telefono_opt,
            "edificios": edificios,
            "data_creatd": data.data_creatd,
            "data_update": data.data_update,
        }
        db.commit()

        return {
            "code": "0",
            "data": info,
            "message": "Administrador listado correctamente",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})
