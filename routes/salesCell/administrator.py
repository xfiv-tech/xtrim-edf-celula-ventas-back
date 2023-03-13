from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db

from model.ModelSchema.salesCellModel import AdministratorModel
from model.SalesCell.administrator import Administrator

from schemas.searchList import SearchList
from datetime import datetime
from middleware.validacionToken import ValidacionToken
from starlette.status import HTTP_204_NO_CONTENT


administrator = APIRouter(route_class=ValidacionToken)

#CITY
@administrator.get("/administradores", tags=["Administradores"])
async def get_administrators():
    try:
        query = Administrator.select()
        data = db.execute(query).fetchall()
        return {
            "list": "Administradores",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}

@administrator.post("/administrador", tags=["Administradores"])
async def add_administrator(administrator: AdministratorModel):
    try:
        result = db.execute(Administrator.insert()
            .values(city = administrator.city,
                    user = administrator.administrator,
                    status = administrator.status,
                    created_at = datetime.now()))
        return {
            "code": "0",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@administrator.put("/administrador", tags=["Administradores"])
async def update_administrator(administrator: AdministratorModel):
    try:
        db.execute(Administrator.update()
            .values(city = administrator.city,
                    user = administrator.administrator,
                    status = administrator.status)
            .where(Administrator.c.id == administrator.id))
        return {
            "code": "0",
            "data": db.execute(Administrator.select()
                        .where(Administrator.c.id == administrator.id))
                        .first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@administrator.delete("/administrador", tags=["Ciudades"])
async def delete_administrator(search: SearchList):
    try:
        db.execute(Administrator.delete()
            .where(Administrator.c.id == search.id))
        return {
            "message": "Administrator successfully deleted"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })