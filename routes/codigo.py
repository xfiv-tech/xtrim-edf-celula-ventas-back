from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from function.CodigoVendedor import ConsultarVendedor, LoginCodigo


codigo = APIRouter()

class CodigoModel(BaseModel):
    codigo: str

@codigo.post("/codigo", tags=["Codigo"])
async def BuscarCoder(data:CodigoModel):
    try:
        print(data)
        response = await ConsultarVendedor(data.codigo)
        return response
    except Exception as e:
        print(e)
        return {"message": "error"}
    
