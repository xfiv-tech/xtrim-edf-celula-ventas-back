from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db
from model.ModelSchema.channelModel import ChanellModel, MandoModel
from model.channel import Channel, Mando
from model.edificio import Edicifios
from schemas.edificio import Edificio
from schemas.edificioList import EdificioList
from datetime import datetime
from model.administrador import Administradores
from middleware.validacionToken import ValidacionToken

from starlette.status import HTTP_204_NO_CONTENT


channel = APIRouter(route_class=ValidacionToken)


@channel.get("/channel", tags=["channel"])
async def get_channel():
    try:
        query = Channel.select()
        data = db.execute(query).fetchall()
        return {
            "code": "0",
            "data": data,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@channel.post("/crear_channel", tags=["channel"])
async def CrearChannel(channel: ChanellModel):
    try:
        query = Channel.insert().values(channel=channel.channel)
        return {
            "code": "0",
            "data": db.execute(query).first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })

@channel.put("/channel", tags=["channel"])
async def create_edificio(channel: ChanellModel):
    try:
        print(channel.id)
        query = Channel.update().values(channel=channel.channel).where(Channel.c.id_channel == channel.id)
        return {
            "code": "0",
            "data": db.execute(query).first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })



@channel.delete("/channel", tags=["channel"])
async def update_channel(channel: ChanellModel):
    try:
        query = Channel.delete().where(Channel.c.id_channel == channel.id)
        return {
            "code": "0",
            "data": db.execute(query).first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@channel.get("/channel/{id}", tags=["channel"])
async def get_channel(id: int):
    try:
        query = Channel.select().where(Channel.c.id_channel == id)
        data = db.execute(query).first()
        return {
            "code": "0",
            "data": data,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })
    

@channel.get("/mando", tags=["mando"])
async def get_mando():
    try:
        query = Mando.select()
        data = db.execute(query).fetchall()
        return {
            "code": "0",
            "data": data,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })

@channel.post("/mando", tags=["mando"])
async def Crearmando(mando: MandoModel):
    try:
        print(mando.id)
        query = Mando.insert().values(mando=mando.mando)
        return {
            "code": "0",
            "data": db.execute(query).first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })

@channel.put("/mando", tags=["mando"])
async def create_mando(mando: MandoModel):
    try:
        print(mando.id)
        query = Mando.update().values(mando=mando.mando).where(Mando.c.id_mando == mando.id)
        return {
            "code": "0",
            "data": db.execute(query).first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@channel.delete("/mando", tags=["mando"])
async def update_mando(mando: MandoModel):
    try:
        query = Mando.delete().where(Mando.c.id_mando == mando.id)
        return {
            "code": "0",
            "data": db.execute(query).first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })

