from fastapi import APIRouter, HTTPException
from database.db import db
from model.ModelSchema.channelModel import (
    ChanellModel,
    CiudadModel,
    EstadosModel,
    GeneroModel,
    MandoModel,
    ModalidadModel,
    OperadorModel,
    SistemaOperativoModel,
)
from model.channel import (
    Perfiles,
    Channel,
    Ciudad,
    Estados,
    Genero,
    Modalidad,
    Operador,
    SistemaOperativo,
)
from middleware.validacionToken import ValidacionToken
from time import time, sleep, strftime, gmtime

channel = APIRouter(route_class=ValidacionToken)


@channel.get("/channel", tags=["channel"])
async def get_channel():
    try:
        result = db.execute(Channel.select()).fetchall()
        data = [dict(row._mapping) for row in result]
        return {
            "code": "0",
            "data": data,
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@channel.post("/crear_channel", tags=["channel"])
async def CrearChannel(channel: ChanellModel):
    try:
        db.execute(Channel.insert().values(channel=channel.channel))
        return {"code": "0"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@channel.put("/channel", tags=["channel"])
async def create_edificio(channel: ChanellModel):
    try:
        db.execute(
            Channel.update()
            .values(channel=channel.channel)
            .where(Channel.c.id_channel == channel.id)
        )
        return {
            "code": "0",
            "data": db.execute(
                Channel.select().where(Channel.c.id_channel == channel.id)
            ).first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@channel.get("/fecha_actual", tags=["Fecha Actual"])
async def fecha_actual():
    try:
        fecha_actual = strftime("%Y-%m-%d %H:%M:%S")
        return {"code": "0", "data": fecha_actual}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


# @channel.delete("/channel", tags=["channel"])
# async def update_channel(channel: ChanellModel):
#     try:
#         db.execute(Channel.delete().where(Channel.c.id_channel == channel.id))
#         return {
#             "code": "0"
#         }
#     except Exception as e:
#         raise HTTPException(status_code=400, detail={
#             "code": "-1",
#             "data": str(e)
#         })


@channel.get("/channel/{id}", tags=["channel"])
async def get_channel(id: int):
    try:
        result = db.execute(Channel.select().where(Channel.c.id_channel == id)).first()
        data = dict(result) if result else {}
        print("data channelById", data)
        return {
            "code": "0",
            "data": data,
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


# Ciudad
@channel.get("/ciudad", tags=["ciudad"])
async def get_ciudad():
    try:
        result = db.execute(Ciudad.select()).fetchall()
        data = [dict(row._mapping) for row in result]
        return {
            "code": "0",
            "data": data,
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@channel.post("/ciudad", tags=["ciudad"])
async def crear_ciudad(ciudad: CiudadModel):
    try:
        db.execute(Ciudad.insert().values(ciudad=ciudad.ciudad, region=ciudad.region))
        return {"code": "0"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@channel.put("/ciudad", tags=["ciudad"])
async def update_ciudad(ciudad: CiudadModel):
    try:
        db.execute(
            Ciudad.update()
            .values(ciudad=ciudad.ciudad, region=ciudad.region)
            .where(Ciudad.c.id_ciudad == ciudad.id)
        )
        updated_result = db.execute(
            Ciudad.select().where(Ciudad.c.id_ciudad == ciudad.id)
        ).first()
        print(f"Updated result: {updated_result}")
        print(f"Type of updated result: {type(updated_result)}")

        if isinstance(updated_result, dict):
            data = updated_result
        elif isinstance(updated_result, tuple):
            data = dict(zip(Ciudad.c.keys(), updated_result))

        return {
            "code": "0",
            "data": data,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


# @channel.delete("/ciudad", tags=["ciudad"])
# async def delete_cuidad(ciudad: CiudadModel):
#     try:
#         db.execute(Ciudad.delete().where(Ciudad.c.id_ciudad == ciudad.id))
#         return {
#             "code": "0"
#         }
#     except Exception as e:
#         raise HTTPException(status_code=400, detail={
#             "code": "-1",
#             "data": str(e)
#         })


# Operador


@channel.get("/operador", tags=["operador"])
async def get_operador():
    try:
        result = db.execute(Operador.select()).fetchall()
        data = [dict(row._mapping) for row in result]
        return {
            "code": "0",
            "data": data,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@channel.post("/operador", tags=["operador"])
async def CrearOperador(operador: OperadorModel):
    try:
        db.execute(Operador.insert().values(operador=operador.operador))
        return {"code": "0"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@channel.put("/operador", tags=["operador"])
async def create_operador(operador: OperadorModel):
    try:
        db.execute(
            Operador.update()
            .values(operador=operador.operador)
            .where(Operador.c.id_operador == operador.id)
        )
        return {
            "code": "0",
            "data": db.execute(
                Operador.select().where(Operador.c.id_operador == operador.id)
            ).first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})

    # @channel.delete("/operador", tags=["operador"])
    # async def delete_operador(operador: OperadorModel):
    try:
        db.execute(Operador.delete().where(Operador.c.id_operador == operador.id))
        return {"code": "0"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


# SistemaOperativo
@channel.get("/sistemaoperativo", tags=["sistemaoperativo"])
async def get_sistemaoperativo():
    try:
        result = db.execute(SistemaOperativo.select()).fetchall()
        data = [dict(row._mapping) for row in result]
        return {
            "code": "0",
            "data": data,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@channel.post("/sistemaoperativo", tags=["sistemaoperativo"])
async def CrearSistemaOperativo(sistemaoperativo: SistemaOperativoModel):
    try:
        db.execute(
            SistemaOperativo.insert().values(
                sistema_operativo=sistemaoperativo.sistema_operativo
            )
        )
        return {"code": "0"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@channel.put("/sistemaoperativo", tags=["sistemaoperativo"])
async def create_sistemaoperativo(sistemaoperativo: SistemaOperativoModel):
    try:
        db.execute(
            SistemaOperativo.update()
            .values(sistema_operativo=sistemaoperativo.sistema_operativo)
            .where(SistemaOperativo.c.id_sistema_operativo == sistemaoperativo.id)
        )
        return {
            "code": "0",
            "data": db.execute(
                SistemaOperativo.select().where(
                    SistemaOperativo.c.id_sistema_operativo == sistemaoperativo.id
                )
            ).first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})

    # @channel.delete("/sistemaoperativo", tags=["sistemaoperativo"])
    # async def delete_sistemaoperativo(sistemaoperativo: SistemaOperativoModel):
    try:
        db.execute(
            SistemaOperativo.delete().where(
                SistemaOperativo.c.id_sistema_operativo == sistemaoperativo.id
            )
        )
        return {"code": "0"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


# Estados
@channel.get("/estado", tags=["estado"])
async def get_estado():
    try:
        result = db.execute(Estados.select()).fetchall()
        data = [dict(row._mapping) for row in result]
        return {
            "code": "0",
            "data": data,
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@channel.post("/estado", tags=["estado"])
async def CrearEstado(estado: EstadosModel):
    try:
        db.execute(Estados.insert().values(estado=estado.estado))
        return {"code": "0"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@channel.put("/estado", tags=["estado"])
async def create_estado(estado: EstadosModel):
    try:
        db.execute(
            Estados.update()
            .values(estado=estado.estado)
            .where(Estados.c.id_estado == estado.id)
        )
        return {
            "code": "0",
            "data": db.execute(
                Estados.select().where(Estados.c.id_estado == estado.id)
            ).first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


# @channel.delete("/estado", tags=["estado"])
# async def delete_estado(estado: EstadosModel):
#     try:
#         db.execute(Estados.delete().where(Estados.c.id_estado == estado.id))
#         return {
#             "code": "0"
#         }
#     except Exception as e:
#         raise HTTPException(status_code=400, detail={
#             "code": "-1",
#             "data": str(e)
#         })


# Genero
@channel.get("/genero", tags=["genero"])
async def get_genero():
    try:
        result = db.execute(Genero.select()).fetchall()
        data = [dict(row._mapping) for row in result]
        return {
            "code": "0",
            "data": data,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@channel.post("/genero", tags=["genero"])
async def CrearGenero(genero: GeneroModel):
    try:
        db.execute(Genero.insert().values(genero=genero.genero))
        return {"code": "0"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@channel.put("/genero", tags=["genero"])
async def create_genero(genero: GeneroModel):
    try:
        db.execute(
            Genero.update()
            .values(genero=genero.genero)
            .where(Genero.c.id_genero == genero.id)
        )
        return {
            "code": "0",
            "data": db.execute(
                Genero.select().where(Genero.c.id_genero == genero.id)
            ).first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


# @channel.delete("/genero", tags=["genero"])
# async def delete_genero(genero: GeneroModel):
#     try:
#         db.execute(Genero.delete().where(Genero.c.id_genero == genero.id))
#         return {
#             "code": "0"
#         }
#     except Exception as e:
#         raise HTTPException(status_code=400, detail={
#             "code": "-1",
#             "data": str(e)
#         })


# Modalidad
@channel.get("/modalidad", tags=["modalidad"])
async def get_modalidad():
    try:
        result = db.execute(Modalidad.select()).fetchall()
        data = [dict(row._mapping) for row in result]
        return {
            "code": "0",
            "data": data,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@channel.post("/modalidad", tags=["modalidad"])
async def CrearModalidad(modalidad: ModalidadModel):
    try:
        db.execute(Modalidad.insert().values(modalidad=modalidad.modalidad))
        return {"code": "0"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@channel.put("/modalidad", tags=["modalidad"])
async def create_modalidad(modalidad: ModalidadModel):
    try:
        db.execute(
            Modalidad.update()
            .values(modalidad=modalidad.modalidad)
            .where(Modalidad.c.id_modalidad == modalidad.id)
        )
        return {
            "code": "0",
            "data": db.execute(
                Modalidad.select().where(Modalidad.c.id_modalidad == modalidad.id)
            ).first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


# @channel.delete("/modalidad", tags=["modalidad"])
# async def delete_modalidad(modalidad: ModalidadModel):
#     try:
#         db.execute(Modalidad.delete().where(Modalidad.c.id_modalidad == modalidad.id))
#         return {
#             "code": "0"
#         }
#     except Exception as e:
#         raise HTTPException(status_code=400, detail={
#             "code": "-1",
#             "data": str(e)
#         })


@channel.get("/perfil", tags=["Perfils"])
async def get_perfil():
    try:
        result = db.execute(Perfiles.select()).fetchall()
        data = [dict(row._mapping) for row in result]
        return {
            "code": "0",
            "data": data,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})
