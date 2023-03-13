from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db
from model.ModelSchema.channelModel import CatalogModel, CatalogDetailModel, ListCatalog, ListCatalogDetail
from model.catalogs import Catalog, CatalogDetail
from schemas.searchList import SearchList
from datetime import datetime
from middleware.validacionToken import ValidacionToken
from utils.HTTPResponse import response_400, response_data_200
from starlette.status import HTTP_204_NO_CONTENT


catalogs = APIRouter(route_class=ValidacionToken)

#CATALOGS
@catalogs.get("/catalogos", tags=["Catalogos"])
async def get_catalogs():
    try:
        query = Catalog.select()
        data = db.execute(query).fetchall()
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}


@catalogs.post("/catalogo", tags=["Catalogos"])
async def add_catalog(catalog: CatalogModel):
    try:
        result = db.execute(Catalog.insert()
            .values(name = catalog.name,
                    code = catalog.code))
        return {
            "code": "0",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@catalogs.put("/catalogo", tags=["Catalogos"])
async def update_catalog(catalog: CatalogModel):
    try:
        db.execute(Catalog.update()
            .values(name = catalog.name)
            .where(Catalog.c.id == catalog.id))
        return {
            "code": "0",
            "data": db.execute(Catalog.select()
                        .where(Catalog.c.id == catalog.id))
                        .first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@catalogs.delete("/catalogo", tags=["Catalogos"])
async def delete_catalog(catalog: CatalogModel):
    try:
        db.execute(Catalog.delete()
            .where(Catalog.c.id == catalog.id))
        return {
            "code": "0"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })

#CATALOG DETAILS
@catalogs.get("/detalle_catalogos", tags=["Detalle de catalogo"])
async def get_catalogDetails():
    try:
        query = CatalogDetail.join(Catalog).select()
        data = db.execute(query).fetchall()
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}


@catalogs.post("/detalle_catalogo", tags=["Detalle de catalogo"])
async def add_catalog(catalogDetail: CatalogDetailModel):
    try:
        result = db.execute(CatalogDetail.insert()
            .values(name = catalogDetail.name,
                    code = catalogDetail.code,
                    level = catalogDetail.level,
                    description = catalogDetail.description,
                    catalog = catalogDetail.catalog))
        return {
            "code": "0",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


#CATALOD DETAILS BY CATALOG ID
@catalogs.get("/detalle_por_catalogo", tags=["Detalle de catalogo"])
async def get_catalogDetails(search: SearchList):
    try:
        query = CatalogDetail.join(Catalog).select().where(CatalogDetail.c.catalog == search.id)
        data = db.execute(query).fetchall()
        return {
            "code": "Catalog Details",
            "data": data }
    except Exception as e:
        return {"error": str(e)}