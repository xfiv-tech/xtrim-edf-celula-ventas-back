from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db
from middleware.validacionToken import ValidacionToken
from model.ModelSchema.roles import RoleBase
from model.roles import Roles


roles = APIRouter(route_class=ValidacionToken)


@roles.post("/roles", tags=["roles"])
async def create_roles(rol: RoleBase):
    try:
        if db.execute(Roles.select().where(Roles.c.rol == rol.rol)).first():
            return {"code": "-1", "data": "El rol ya existe"}
        else:
            db.execute(Roles.insert().values(rol=rol.rol, descripcion=rol.descripcion))
            db.commit()
            return {"code": "0", "message": "Rol creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e.args)})


@roles.get("/roles", tags=["roles"])
async def get_rol():
    try:
        result = db.execute(Roles.select()).fetchall()
        data = [dict(row._mapping) for row in result]
        return {"code": "0", "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@roles.put("/roles", tags=["roles"])
async def update_rol(rol: RoleBase):
    try:
        data = db.execute(
            Roles.update()
            .where(Roles.c.id_roles == rol.id)
            .values(rol=rol.rol, descripcion=rol.descripcion)
        )
        db.commit()
        return {"code": "0", "data": data, "message": "Rol actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@roles.delete("/roles", tags=["roles"])
async def delete_rol(rol: RoleBase):
    try:
        db.execute(Roles.delete().where(Roles.c.id_roles == rol.id))
        db.commit()
        return {"code": "0", "message": "Rol eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})
