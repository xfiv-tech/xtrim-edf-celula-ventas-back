from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db
from model.ModelSchema.channelModel import CatalogModel, CatalogDetailModel, ListCatalog, ListCatalogDetail, RegistrarVendedorModel
from model.channel import RegistrarDistribuidor, Channel, RegistrarVendedor, Ciudad
from schemas.searchList import SearchList
from datetime import datetime
from middleware.validacionToken import ValidacionToken
from utils.HTTPResponse import response_400, response_data_200
from starlette.status import HTTP_204_NO_CONTENT


operations = APIRouter(route_class=ValidacionToken)

@operations.get("/distribuitorByOtherRoute", tags=["Catalog Details"])
async def get_distribuitor():
    try:
        query = RegistrarDistribuidor.join(Channel).select()
        data = db.execute(query).fetchall()
        return {
            "code": "Cities",
            "data": data }
    except Exception as e:
        return {"error": str(e)}
    

@operations.get("/sellerByOtherRoute", tags=["Vendedor"])
async def get_registro():
    try:
        query = RegistrarVendedor.join(Ciudad).select()
        data = db.execute(query).fetchall()
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}