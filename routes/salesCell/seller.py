from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db

from model.ModelSchema.salesCellModel import SellerModel, CityModel
from model.SalesCell.seller import Seller
from model.SalesCell.city import City
from model.SalesCell.employee import Employee

from schemas.searchList import SearchList
from datetime import datetime
from middleware.validacionToken import ValidacionToken
from starlette.status import HTTP_204_NO_CONTENT


seller = APIRouter(route_class=ValidacionToken)

#SELLER
@seller.get("/vendedores", tags=["Vendedores"])
async def get_sellers():
    try:
        query = Seller.select()
        data = db.execute(query).fetchall()
        return {
            "list": "Vendedores",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}

@seller.get("/lista_vendedores", tags=["Vendedores"])
async def get_sellers():
    try:
        query = Seller.join(Employee).select().with_only_columns([
            Seller.c.id,
            Seller.c.seller,
            Employee.c.name.label('employee_name'),
            Employee.c.lastname.label('employee_name'),
            Seller.c.equifax_user,
            Seller.c.goal_volumen,
            Seller.c.goal_dolars
        ])
        return {
            "message": "Catalog detail retrieved successfully",
            "data": db.execute(query).all(),
        }
    except Exception as e:
        return {"error": str(e)}


@seller.post("/vendedor", tags=["Vendedores"])
async def add_seller(seller: SellerModel):
    try:
        result = db.execute(Seller.insert()
            .values(seller = seller.seller,
                    equifax_user = seller.equifax_user,
                    city = seller.city,
                    channel = seller.channel,
                    modality = seller.modality,
                    goal_volumen = seller.goal_volumen,
                    goal_dolars = seller.goal_dolars,
                    os = seller.os,
                    status = seller.status,
                    date_in_sales_dept = seller.date_in_sales,
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


@seller.put("/vendedor", tags=["Vendedores"])
async def update_seller(seller: SellerModel):
    try:
        db.execute(Seller.update()
            .values(seller = seller.seller,
                    equifax_user = seller.equifax_user,
                    city = seller.city,
                    channel = seller.channel,
                    modality = seller.modality,
                    goal_volumen = seller.goal_volumen,
                    goal_dolars = seller.goal_dolars,
                    os = seller.os,
                    status = seller.status,
                    date_out_sales_dept = seller.date_out_sales_dept,
                    created_at = datetime.now())
            .where(Seller.c.id == seller.id))
        return {
            "code": "0",
            "data": db.execute(Seller.select()
                        .where(Seller.c.id == seller.id))
                        .first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@seller.delete("/vendedor", tags=["Vendedores"])
async def delete_seller(search: SearchList):
    try:
        db.execute(Seller.delete()
            .where(Seller.c.id == search.id))
        return {
            "message": "Seller successfully deleted"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })