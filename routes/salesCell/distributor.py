from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db

from model.ModelSchema.salesCellModel import DistributorModel
from model.SalesCell.distributor import Distributor

from schemas.searchList import SearchList
from datetime import datetime
from middleware.validacionToken import ValidacionToken
from starlette.status import HTTP_204_NO_CONTENT


distributor = APIRouter(route_class=ValidacionToken)

#DISTRIBUTOR
@distributor.get("/distribuidores", tags=["Distribuidores"])
async def get_distributor():
    try:
        query = Distributor.select()
        data = db.execute(query).fetchall()
        return {
            "list": "Distribuidores",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}


@distributor.post("/distribuidor", tags=["Distribuidores"])
async def add_distributor(distributor: DistributorModel):
    try:
        result = db.execute(Distributor.insert()
            .values(name = distributor.name,
                    city = distributor.city,
                    responsible = distributor.responsible,
                    status = distributor.status,
                    phone = distributor.phone,
                    email = distributor.email,
                    date_in = distributor.date_in,
                    date_out = distributor.date_out))
        return {
            "code": "0",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@distributor.put("/distribuidor", tags=["Distribuidores"])
async def update_distributor(distributor: DistributorModel):
    try:
        db.execute(Distributor.update()
            .values(name = distributor.name,
                    city = distributor.city,
                    responsible = distributor.responsible,
                    status = distributor.status,
                    phone = distributor.phone,
                    email = distributor.email,
                    date_in = distributor.date_in,
                    date_out = distributor.date_out)
            .where(Distributor.c.id == distributor.id))
        return {
            "code": "0",
            "data": db.execute(Distributor.select()
                        .where(Distributor.c.id == distributor.id))
                        .first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@distributor.delete("/distribuidor", tags=["Distribuidores"])
async def delete_distributor(search: SearchList):
    try:
        db.execute(Distributor.delete()
            .where(Distributor.c.id == search.id))
        return {
            "message": "Distributor successfully deleted"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })