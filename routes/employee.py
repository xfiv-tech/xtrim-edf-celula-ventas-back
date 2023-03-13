from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db

from model.ModelSchema.channelModel import CatalogModel, CatalogDetailModel, ListCatalog, ListCatalogDetail
from model.catalogs import Catalog, CatalogDetail

from model.ModelSchema.salesCellModel import EmployeeModel
from model.SalesCell.employee import Employee

from schemas.searchList import SearchList
from datetime import datetime
from middleware.validacionToken import ValidacionToken
from utils.HTTPResponse import response_400, response_data_200
from starlette.status import HTTP_204_NO_CONTENT


employee = APIRouter(route_class=ValidacionToken)

#CATALOGS
@employee.get("/empleadosWithRelations", tags=["Empleados"])
async def get_employeesWithRelations():
    try:
        operator = CatalogDetail.alias('operator')
        gender = CatalogDetail.alias('gender')
        status = CatalogDetail.alias('status')

        join_cond = (Employee.c.operator == operator.c.id) & (Employee.c.gender == gender.c.id) & (Employee.c.status == status.c.id)

        employee_join = Employee.join(Employee.c.operator == CatalogDetail.c.id)

        # Consulta para obtener toda la información relacionada entre las tablas "Employee" y "catalog_detail"
        query = Employee.select([employee, operator, gender, status]).\
                select_from(employee_join).\
                where(join_cond)
        data = db.execute(query).fetchall()
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}
    
@employee.get("/empleados", tags=["Detalle de catalogo"])
async def get_employes():
    try:
        query = Employee.select()
        data = db.execute(query).fetchall()
        return {
            "list": "Empleaddos",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}


@employee.post("/empleado", tags=["Empleados"])
async def add_catalog(employee: EmployeeModel):
    try:
        result = db.execute(Employee.insert()
            .values(name = employee.name,
                    lastname = employee.lastname,
                    id_number = employee.id_number,
                    address = employee.address,
                    residence_city = employee.residence_city,
                    birth_date = employee.birth_date,
                    email = employee.email,
                    phone = employee.phone,
                    operator = employee.operator,
                    phone_optional = employee.phone_optional,
                    operator_optional = employee.operator_optional,
                    gender = employee.gender,
                    status = employee.status,
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


@employee.put("/empleado", tags=["Empleados"])
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


@employee.delete("/catalog", tags=["Empleados"])
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




#CATALOD DETAILS BY CATALOG ID
""" @employee.get("/employe_by_catalog", tags=["Catalog Details"])
async def get_catalogDetails(search: SearchList):
    try:
        query = CatalogDetail.join(Catalog).select().where(CatalogDetail.c.catalog == search.id)
        data = db.execute(query).fetchall()
        return {
            "code": "Catalog Details",
            "data": data }
    except Exception as e:
        return {"error": str(e)} """