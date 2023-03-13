from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db

from model.ModelSchema.salesCellModel import CityModel
from model.SalesCell.city import City

from schemas.searchList import SearchList
from datetime import datetime
from middleware.validacionToken import ValidacionToken
from starlette.status import HTTP_204_NO_CONTENT


city = APIRouter(route_class=ValidacionToken)

#CITY
@city.get("/ciudades", tags=["Ciudades"])
async def get_cities():
    try:
        query = City.select()
        data = db.execute(query).fetchall()
        return {
            "list": "Ciudades",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}

@city.post("/ciudad", tags=["Ciudades"])
async def add_city(city: CityModel):
    try:
        result = db.execute(City.insert()
            .values(name = city.name,
                    type = city.type,
                    region = city.region,
                    status = city.status,
                    manager_region = city.manager_region,
                    manager_city = city.manager_city,
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


@city.put("/ciudad", tags=["Ciudades"])
async def update_city(city: CityModel):
    try:
        db.execute(City.update()
            .values(name = city.name,
                    type = city.type,
                    region = city.region,
                    status = city.status,
                    manager_region = city.manager_region,
                    manager_city = city.manager_city)
            .where(City.c.id == city.id))
        return {
            "code": "0",
            "data": db.execute(City.select()
                        .where(City.c.id == city.id))
                        .first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@city.delete("/ciudad", tags=["Ciudades"])
async def delete_city(search: SearchList):
    try:
        db.execute(City.delete()
            .where(City.c.id == search.id))
        return {
            "message": "City successfully deleted"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })