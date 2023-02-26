from middleware.validacionToken import ValidacionToken
from fastapi import APIRouter, Request, HTTPException
from model.ModelSchema.menu import MenuBase, SubmenuBase
from model.menu import Menus
from model.submenu import Submenus
from database.db import db

menu = APIRouter(
    route_class=ValidacionToken,
    tags=["Menu"],
)

@menu.get("/menu", tags=["menu"])
async def get_menu():
    try:
        data = db.execute(Menus.select()).fetchall()
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })
    
@menu.post("/menu", tags=["menu"])
async def post_menu(menu: MenuBase):
    try:
        data = db.execute(Menus.insert().values(
            id_roles=menu.id_roles,
            menu=menu.menu,
            path=menu.path,
            icon=menu.icon
        )).inserted_primary_key
        for submenu in menu.submenus:
            db.execute(Submenus.insert().values(
                id_menus=data[0],
                submenu=submenu.submenu,
                path=submenu.path,
                icon=submenu.icon
            ))
        return {
            "code": "0",
            "data": "Menu creado"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })



@menu.post("/submenu", tags=["menu"])
async def post_submenu(submenu: SubmenuBase):
    try:
        db.execute(Submenus.insert().values(
            id_menus=submenu.id_menus,
            submenu=submenu.submenu,
            path=submenu.path,
            icon=submenu.icon
        ))
        return {
            "code": "0",
            "data": "Submenu creado"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@menu.put("/submenu", tags=["menu"])
async def put_submenu(submenu: SubmenuBase):
    try:
        db.execute(Submenus.update().where(Submenus.c.id == submenu.id).values(
            id_menus=submenu.id_menus,
            path=submenu.path,
            icon=submenu.icon
        ))
        return {
            "code": "0",
            "data": "Submenu actualizado"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })
    
@menu.delete("/submenu/{id}", tags=["menu"])
async def delete_submenu(id: int):
    try:
        db.execute(Submenus.delete().where(Submenus.c.id == id))
        return {
            "code": "0",
            "data": "Submenu eliminado"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })
