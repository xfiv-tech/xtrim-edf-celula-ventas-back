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
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

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
            print("i_menus", i.menu)
            exc = Submenus.select().where(Submenus.c.id_menus == i.id_menus)
            sub = db.execute(exc).fetchall()
            info_menu.append(
                {
                    "id_menus": i.id_menus,
                    "menu": i.menu,
                    "path": i.path,
                    "icon": i.icon,
                    "submenu": sub,
                }
            )
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
                    "message": "Login correcto",
                }
            else:
                return {"code": "-1", "data": [], "message": "Contraseña incorrecta"}
        else:
            return {"code": "-1", "data": [], "message": "Usuario no existe"}
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e.args)})


@login.post("/login_celula", tags=["login"])
async def ValidacionLoginCelula(datos: Login):
    try:
        # Realiza la consulta para verificar el usuario
        query = RegistroAdministrador.select().where(
            RegistroAdministrador.c.email == datos.email
        )
        user = db.execute(query).first()

        if user is None:
            return {"code": "-1", "data": [], "message": "Usuario no existe"}

        # Verifica la contraseña
        decr_data = checkPassword(datos.password, user.password)
        if not decr_data:
            return {"code": "-1", "data": [], "message": "Contraseña incorrecta"}

        # Obtiene el menú
        menu_query = Menus.select().where(Menus.c.id_roles == user.id_roles)
        menu = db.execute(menu_query).fetchall()

        info_menu = []
        for i in menu:
            exc = Submenus.select().where(Submenus.c.id_menus == i.id_menus)
            sub = db.execute(exc).fetchall()

            submenus_data = []
            for s in sub:
                submenus_data.append(
                    {
                        "id_submenu": s[0],
                        "submenu": s[2],
                        "path": s[3],
                        "icon": s[4],
                    }
                )

            info_menu.append(
                {
                    "id_menus": i.id_menus,
                    "menu": i.menu,
                    "path": i.path,
                    "icon": i.icon,
                    "submenu": submenus_data,
                }
            )

        true_user = {
            "id": user.id_administrador,
            "id_rol": user.id_roles,
            "email": user.email,
            "usuario": user.nombre_administrador,
            "perfil": user.perfil,
        }

        # Retorna los datos si todo salió bien
        return {
            "code": "0",
            "token": write_token(true_user),
            "menu": info_menu,
            "message": "Login correcto",
        }

    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e.args)})

    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})
