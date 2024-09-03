from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db
from model.edificio import Edicifios
from schemas.edificio import Edificio
from schemas.edificioList import EdificioList
from datetime import datetime
from model.administrador import Administradores
from middleware.validacionToken import ValidacionToken

# from starlette.status import HTTP_204_NO_CONTENT


edificios = APIRouter(
    route_class=ValidacionToken,
    tags=["Edificios"],
)


@edificios.post("/edificios", tags=["edificios"])
async def get_edificios():
    try:
        query = (
            Edicifios.join(Administradores)
            .select()
            .with_only_columns(
                Edicifios.c.id,
                Edicifios.c.idAdministrador,
                Administradores.c.nombreAdministrador,
                Edicifios.c.id_edificio,
                Edicifios.c.sector,
                Edicifios.c.ciudad,
                Edicifios.c.coordenadas,
                Edicifios.c.ctaReferencia,
                Edicifios.c.cedulaReferencia,
                Edicifios.c.nombreEdificio,
                Edicifios.c.referencia,
                Edicifios.c.responsable,
                Edicifios.c.adjunto,
                Edicifios.c.data_creatd,
                Edicifios.c.data_update,
            )
        )
        data = db.execute(query).fetchall()
        return {
            "code": "0",
            "data": data,
            "message": "Edificios listados correctamente",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@edificios.post("/edificios_listar/", tags=["edificios"])
async def edificioID(edificioID: EdificioList):
    try:
        print(edificioID.id)
        # query = db.execute(Edicifios.select().where(Edicifios.c.id == edificioID.id)).first()
        query = (
            Edicifios.join(Administradores)
            .select()
            .with_only_columns(
                Edicifios.c.id,
                Edicifios.c.idAdministrador,
                Administradores.c.nombreAdministrador,
                Edicifios.c.id_edificio,
                Edicifios.c.sector,
                Edicifios.c.ciudad,
                Edicifios.c.coordenadas,
                Edicifios.c.ctaReferencia,
                Edicifios.c.cedulaReferencia,
                Edicifios.c.nombreEdificio,
                Edicifios.c.referencia,
                Edicifios.c.responsable,
                Edicifios.c.adjunto,
                Edicifios.c.data_creatd,
                Edicifios.c.data_update,
            )
            .where(Edicifios.c.id == edificioID.id)
        )
        # query = db.execute(query).first()
        return {
            "code": "0",
            "data": db.execute(query).first(),
            "message": "Edificio encontrado",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@edificios.post("/edificios_crear", tags=["edificios"])
async def create_edificio(edificio: Edificio):

    latitud = edificio.coordenadas.split(",")[0]
    longitud = edificio.coordenadas.split(",")[1]

    new_edificio = {
        "id_usuario": edificio.id_usuario,
        "idAdministrador": edificio.idAdministrador,
        "id_edificio": edificio.id_edificio,
        "sector": edificio.sector,
        "ciudad": edificio.ciudad,
        "coordenadas": f"https://maps.google.com/?q={latitud},{longitud}",
        "ctaReferencia": edificio.ctaReferencia,
        "cedulaReferencia": edificio.cedulaReferencia,
        "nombreEdificio": edificio.nombreEdificio,
        "referencia": edificio.referencia,
        "responsable": edificio.responsable,
        "adjunto": edificio.adjunto,
        "data_creatd": datetime.now(),
    }
    try:
        db.execute(Edicifios.insert().values(new_edificio))
        data = db.execute(Edicifios.select()).fetchall()
        return {"code": "0", "data": data, "message": "Edificio creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@edificios.put("/edificios_actualizar", tags=["edificios"])
async def update_edificio(edificio: Edificio):
    try:
        latitud = edificio.coordenadas.split(",")[0]
        longitud = edificio.coordenadas.split(",")[1]

        db.execute(
            Edicifios.update()
            .values(
                idAdministrador=edificio.idAdministrador,
                id_edificio=edificio.id_edificio,
                sector=edificio.sector,
                ciudad=edificio.ciudad,
                coordenadas=f"https://maps.google.com/?q={latitud},{longitud}",
                ctaReferencia=edificio.ctaReferencia,
                cedulaReferencia=edificio.cedulaReferencia,
                nombreEdificio=edificio.nombreEdificio,
                referencia=edificio.referencia,
                responsable=edificio.responsable,
                adjunto=edificio.adjunto,
                data_update=datetime.now(),
            )
            .where(Edicifios.c.idAdministrador == edificio.id)
        )
        data = db.execute(Edicifios.select()).fetchall()
        return {
            "code": "0",
            "data": data,
            "message": "Edificio actualizado correctamente",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@edificios.delete("/edificios_eliminar", tags=["edificios"])
async def delete_edificio(edificioID: EdificioList):
    try:
        db.execute(Edicifios.delete().where(Edicifios.c.id == edificioID.id))
        return {"code": "0", "data": [], "message": "Edificio eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})
