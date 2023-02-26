from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db
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

usuarios = APIRouter(
    route_class=ValidacionToken,
    tags=["Usuarios"],
)

@usuarios.post("/usuarios", tags=["usuarios"])
async def get_usuarios():
    try:
        query = Usuarios.select()
        data = db.execute(query).fetchall()
        return {
            "code": "0",
            "data": data,
            "message": "Edificio actualizado correctamente"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@usuarios.post("/usuarios_lista", tags=["usuarios"])
async def get_usuario(usuarioID: UsuarioList):
    try:
        data = db.execute(Usuarios.select().where(Usuarios.c.id == usuarioID.id)).first()
        return {
            "code": "0",
            "data": data,
            "message": "Edificio actualizado correctamente"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


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
        return {
            "code": "0",
            "data": data,
            "message": "Edificio actualizado correctamente"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@usuarios.put("/usuarios_actualizar", tags=["usuarios"])
async def update_usuario(usuario: Usuario):
    try:
        if len(usuario.password) == 0:
            db.execute(
                Usuarios.update().values(
                    nombreCompleto=usuario.nombreCompleto,
                    email=usuario.email,
                    usuario=usuario.usuario,
                    data_update=datetime.now(),
                ).where(Usuarios.c.id == usuario.id)
            )
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
        return db.execute(Usuarios.select()).fetchall()
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })
    



@usuarios.delete("/usuarios_eliminar", status_code=status.HTTP_204_NO_CONTENT, tags=["usuarios"])
async def delete_usuario(usuarioID: UsuarioList):
    try:
        db.execute(Usuarios.delete().where(Usuarios.c.id == usuarioID.id))
        return {}
    except Exception as e:
        raise {
            "code": "-1",
            "data": str(e)
        }


@usuarios.post("/login", tags=["login"])
async def login(datos: Login):
    try:
        query = Usuarios.select().where(Usuarios.c.email == datos.email)
        user = db.execute(query).first()
        print(user)
        decr_data = checkPassword(datos.password, user[5])
        
        if len(user) > 0:
            if decr_data == True:
                true_user = {
                    "id": user[0],
                    "id_rol": user[1],
                    "nombreCompleto": user[2],
                    "email": user[3],
                    "usuario": user[4],
                    "data_creatd": user[6],
                    "data_update": user[7],
                }
                return {
                    "code": "0",
                    "data": true_user,
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
            "data": str(e)
        })