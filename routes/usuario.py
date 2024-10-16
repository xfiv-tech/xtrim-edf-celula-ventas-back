from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db
from function.function_jwt import write_token
from model.menu import Menus
from model.submenu import Submenus
from model.usuario import Usuarios
from schemas.usuario import Usuario
from schemas.usuarioList import UsuarioList
from schemas.login import Login
from datetime import datetime

from cryptography.fernet import Fernet
from function.encrytPassword import encryptPassword, checkPassword
from starlette.status import HTTP_204_NO_CONTENT
from middleware.validacionToken import ValidacionToken


key = Fernet.generate_key()
f = Fernet(key)

usuarios = APIRouter(route_class=ValidacionToken)


@usuarios.post("/usuarios", tags=["usuarios"])
async def get_usuarios():
    try:
        query = Usuarios.select()
        data = db.execute(query).fetchall()
        return {
            "code": "0",
            "data": data,
            "message": "Edificio actualizado correctamente",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@usuarios.post("/usuarios_lista", tags=["usuarios"])
async def get_usuario(usuarioID: UsuarioList):
    try:
        data = db.execute(
            Usuarios.select().where(Usuarios.c.id == usuarioID.id)
        ).first()
        return {
            "code": "0",
            "data": data,
            "message": "Edificio actualizado correctamente",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@usuarios.post("/usuarios_crear", tags=["usuarios"])
async def create_usuario(usuario: Usuario):
    new_user = {
        "nombreCompleto": usuario.nombreCompleto,
        "email": usuario.email,
        "usuario": usuario.usuario,
        "password": encryptPassword(usuario.password),
        "data_creatd": datetime.now(),
    }
    try:
        db.execute(Usuarios.insert().values(new_user))
        data = db.execute(Usuarios.select()).fetchall()
        db.commit()
        return {
            "code": "0",
            "data": data,
            "message": "Edificio actualizado correctamente",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e)})


@usuarios.put("/usuarios_actualizar", tags=["usuarios"])
async def update_usuario(usuario: Usuario):
    try:
        if len(usuario.password) == 0:
            db.execute(
                Usuarios.update()
                .values(
                    nombreCompleto=usuario.nombreCompleto,
                    email=usuario.email,
                    usuario=usuario.usuario,
                    data_update=datetime.now(),
                )
                .where(Usuarios.c.id == usuario.id)
            )
            db.commit()
        else:
            db.execute(
                Usuarios.update()
                .values(
                    nombreCompleto=usuario.nombreCompleto,
                    email=usuario.email,
                    usuario=usuario.usuario,
                    password=encryptPassword(usuario.password),
                    data_update=datetime.now(),
                )
                .where(Usuarios.c.id == usuario.id)
            )
            db.commit()
        return db.execute(Usuarios.select()).fetchall()
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "-1", "data": str(e.args)})


@usuarios.delete(
    "/usuarios_eliminar", status_code=status.HTTP_204_NO_CONTENT, tags=["usuarios"]
)
async def delete_usuario(usuarioID: UsuarioList):
    try:
        db.execute(Usuarios.delete().where(Usuarios.c.id == usuarioID.id))
        db.commit()
        return {}
    except Exception as e:
        raise {"code": "-1", "data": str(e)}
