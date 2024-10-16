from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from function.FuncionZonal import (
    DeleteZonal,
    ListarZonalAll,
    RegistrarZonal,
    UpdateZonal,
    ZonalId,
)
from middleware.validacionToken import ValidacionToken

zonal = APIRouter(route_class=ValidacionToken)


class Zonal(BaseModel):
    id_gerente_zonal: Optional[int] = None
    nombre: str
    email: str
    telefono: str
    cedula: str


@zonal.get("/zonal", tags=["Zonal"])
async def ListarZonal():
    try:
        result = await ListarZonalAll()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "-1",
                "data": str(e),
            },
        )


@zonal.post("/crear_zonal", tags=["Zonal"])
async def CrearZonal(data: Zonal):
    try:
        return await RegistrarZonal(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@zonal.get("/zonal_id/{id}", tags=["Zonal"])
async def ListaZonalId(id: int):
    try:
        return await ZonalId(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@zonal.put("/actualizar_zonal", tags=["Zonal"])
async def UpdateRegistroZonal(data: Zonal):
    try:
        return await UpdateZonal(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e.args)})


@zonal.delete(
    "/elimina_zonal/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Zonal"]
)
async def DeleteRegistroZonal(id: int):
    return await DeleteZonal(id)
