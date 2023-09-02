from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from function.FuncionIsla import (DeleteIsla, IslaId, ListarIslaAll,
                                  RegistrarIsla, UpdateIsla)
from middleware.validacionToken import ValidacionToken

isla = APIRouter(route_class=ValidacionToken)

class Isla(BaseModel):
    id: Optional[int] = None
    id_ciudad: int
    isla: str

@isla.get("/isla", tags=["Islas"])
async def ListarIslas():
    try:
        return await ListarIslaAll()
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@isla.post("/crear_isla", tags=["Islas"])
async def CrearIsla(data: Isla):
    try:
        return await RegistrarIsla(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@isla.get("/isla_id/{id}", tags=["Islas"])
async def ListaIslaId(id: int):
    try:
        return await IslaId(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@isla.put("/actualizar_isla", tags=["Islas"])
async def update_usuario(data: Isla):
    try:
        return await UpdateIsla(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e.args)
        })
    

@isla.delete("/elimina_isla/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Islas"])
async def delete_usuario(id: int):
    try:
        return await DeleteIsla(id)
    except Exception as e:
        raise {
            "code": "-1",
            "data": str(e)
        }

