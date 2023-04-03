from fastapi import APIRouter, HTTPException
from database.db import db
from function.function_jwt import write_token
from model.channel import RegistroAdministrador
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
                    "id": user.id,
                    "id_rol": user.id_roles,
                    "nombreCompleto": user.nombre_completo,
                    "email": user.email,
                    "usuario": user.usuario,
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
    

@login.post("/login_celula", tags=["login"])
async def ValidacionLoginCelula(datos: Login):
    try:
        print("datos",datos)
        query = RegistroAdministrador.select().where(RegistroAdministrador.c.email == datos.email)
        user = db.execute(query).first()
        print("user",user)
        decr_data = checkPassword(datos.password, user.password)
        menu = Menus.select().where(Menus.c.id_roles == user.id_roles)
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
                    "id": user.id_administrador,
                    "id_rol": user.id_roles,
                    "email": user.email,
                    "usuario": user.nombre_administrador,
                    "perfil": user.perfil,
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