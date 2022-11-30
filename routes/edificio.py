from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db
from model.edificio import Edicifios
from schemas.edificio import Edificio
from datetime import datetime

from starlette.status import HTTP_204_NO_CONTENT


edificios = APIRouter()

@edificios.get("/edificios", tags=["edificios"])
async def get_edificios():
    try:
        query = Edicifios.select()
        return db.execute(query).fetchall()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@edificios.get("/edificios/{id}", tags=["edificios"])
async def get_edificio(id: int):
    try:
        return db.execute(Edicifios.select().where(Edicifios.c.idAdministrador == id)).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@edificios.post("/edificios", tags=["edificios"])
async def create_edificio(edificio: Edificio):
    latitud = edificio.coordenadas.split(",")[0]
    longitud = edificio.coordenadas.split(",")[1]

    new_edificio = {
        "idAdministrador": edificio.idAdministrador,
        "coordenadas": f"https://maps.google.com/?q=${latitud},${longitud}",
        "ctaReferencia": edificio.ctaReferencia,
        "nombreEdificio": edificio.nombreEdificio,
        "referencia": edificio.referencia,
        "adjunto": edificio.adjunto,
        "data_creatd": datetime.now(),
    }
    try:
        db.execute(Edicifios.insert().values(new_edificio))
        return db.execute(Edicifios.select()).fetchall()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.args))


@edificios.put("/edificios/{id}", tags=["edificios"])
async def update_edificio(id: int, edificio: Edificio):
    try:
        latitud = edificio.coordenadas.split(",")[0]
        longitud = edificio.coordenadas.split(",")[1]

        db.execute(
            Edicifios.update().values(
                idAdministrador=edificio.idAdministrador,
                coordenadas=f"https://maps.google.com/?q=${latitud},${longitud}",
                ctaReferencia=edificio.ctaReferencia,
                nombreEdificio=edificio.nombreEdificio,
                referencia=edificio.referencia,
                adjunto=edificio.adjunto,
                data_update=datetime.now(),
            ).where(Edicifios.c.idAdministrador == id)
        )
        return db.execute(Edicifios.select()).fetchall()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.args))


@edificios.delete("/edificios/{id}", tags=["edificios"])
async def delete_edificio(id: int):
    try:
        db.execute(Edicifios.delete().where(Edicifios.c.idAdministrador == id))
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as e:
        return {"error": str(e.args)}