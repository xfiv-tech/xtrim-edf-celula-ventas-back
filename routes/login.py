from fastapi import APIRouter, HTTPException
from database.db import db
from function.function_jwt import write_token
from model.menu import Menus
from model.submenu import Submenus
from model.usuario import Usuarios
from schemas.login import Login
from cryptography.fernet import Fernet
from function.encrytPassword import checkPassword



key = Fernet.generate_key()
f = Fernet(key)

login = APIRouter()


@login.post("/login", tags=["login"])
async def ValidacionLogin(datos: Login):
    try:
        query = Usuarios.select().where(Usuarios.c.email == datos.email)
        user = db.execute(query).first()
        print("decr_data",user)
        decr_data = checkPassword(datos.password, user[5])
        menu = Menus.select().where(Menus.c.id_roles == user[1])
        menu = db.execute(menu).fetchall()
        info_menu = []
        for i in menu:
            print("i_menus",i.menu)
            exc = Submenus.select().where(Submenus.c.id_menus == i.id_menus)
            sub = db.execute(exc).fetchall()
            info_menu.append({
                "id_menus": i.id_menus,
                "menu": i.menu,
                "path": i.path,
                "icon": i.icon,
                "submenu": sub
            })
        if len(user) > 0:
            if decr_data == True:
                true_user = {
                    "id": user[0],
                    "id_rol": user[1],
                    "nombreCompleto": user[2],
                    "email": user[3],
                    "usuario": user[4],
                }
                return {
                    "code": "0",
                    "token": write_token(dict(true_user)),
                    "menu": info_menu,
                    "message": "Login correcto"
                }
            else:
                return {
                    "code": "-1",
                    "data": [],
                    "message": "Contraseña incorrecta"
                }
        else:
            return {
                "code": "-1",
                "data": [],
                "message": "Usuario no existe"
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e.args)
        })