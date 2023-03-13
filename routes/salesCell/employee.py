from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db

from model.ModelSchema.salesCellModel import EmployeeModel
from model.SalesCell.employee import Employee

from schemas.searchList import SearchList
from datetime import datetime
from middleware.validacionToken import ValidacionToken
from starlette.status import HTTP_204_NO_CONTENT


employee = APIRouter(route_class=ValidacionToken)

#EMPLOYEES
@employee.get("/empleados", tags=["Empleados"])
async def get_employes():
    try:
        query = Employee.select()
        data = db.execute(query).fetchall()
        return {
            "list": "Empleados",
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
async def update_employee(employee: EmployeeModel):
    try:
        db.execute(Employee.update()
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
                    status = employee.status)
            .where(Employee.c.id == employee.id))
        return {
            "code": "0",
            "data": db.execute(Employee.select()
                        .where(Employee.c.id == employee.id))
                        .first(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@employee.delete("/empleado", tags=["Empleados"])
async def delete_employee(search: SearchList):
    try:
        db.execute(Employee.delete()
            .where(Employee.c.id == search.id))
        return {
            "message": "Employee successfully deleted"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })