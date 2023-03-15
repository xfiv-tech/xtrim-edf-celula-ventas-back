from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db

from model.ModelSchema.salesCellModel import ManagerModel
from model.SalesCell.manager import Manager

from schemas.searchList import SearchList
from datetime import datetime
from middleware.validacionToken import ValidacionToken
from starlette.status import HTTP_204_NO_CONTENT


manager = APIRouter(route_class=ValidacionToken)

#CITY
@manager.get("/gerentes", tags=["Gerentes"])
async def get_managers():
    try:
        query = Manager.select()
        data = db.execute(query).fetchall()
        return {
            "list": "Gerentes",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}

@manager.post("/gerente", tags=["Gerentes"])
async def add_manager(manager: ManagerModel):
    try:
        result = db.execute(Manager.insert()
            .values(manager = manager.manager,
                    type = manager.type,
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


