from fastapi import APIRouter, Response, Depends, HTTPException, status
from database.db import db
from model.usuario import Usuarios
from schemas.usuario import Usuario
from schemas.login import Login
from datetime import datetime

from cryptography.fernet import Fernet
from function.encrytPassword import encryptPassword, checkPassword
from starlette.status import HTTP_204_NO_CONTENT



key = Fernet.generate_key()
f = Fernet(key)

usuarios = APIRouter()

@usuarios.get("/usuarios", tags=["usuarios"])
async def get_usuarios():
    try:
        query = Usuarios.select()
        return db.execute(query).fetchall()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@usuarios.get("/usuarios/{id}", tags=["usuarios"])
async def get_usuario(id: int):
    return db.execute(Usuarios.select().where(Usuarios.c.id == id)).first()


@usuarios.post("/usuarios", tags=["usuarios"])
async def create_usuario(usuario: Usuario):
    new_user = {
        "nombreCompleto": usuario.nombreCompleto,
        "email": usuario.email,
        "usuario": usuario.usuario,
        "password": encryptPassword(usuario.password),
        "data_creatd": datetime.now(),
    }
    print(new_user)
    try:
        db.execute(Usuarios.insert().values(new_user))
        return db.execute(Usuarios.select()).fetchall()
    except Exception as e:
        return {"error": str(e.args)}


@usuarios.put("/usuarios/{id}", tags=["usuarios"])
async def update_usuario(id: int, usuario: Usuario):
    try:
        if len(usuario.password) == 0:
            db.execute(
                Usuarios.update().values(
                    nombreCompleto=usuario.nombreCompleto,
                    email=usuario.email,
                    usuario=usuario.usuario,
                    data_update=datetime.now(),
                ).where(Usuarios.c.id == id)
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
                .where(Usuarios.c.id == id)
            )
        return db.execute(Usuarios.select()).fetchall()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    



@usuarios.delete("/usuarios/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["usuarios"])
async def delete_usuario(id: int):
    try:
        db.execute(Usuarios.delete().where(Usuarios.c.id == id))
        return Response(status_code=HTTP_204_NO_CONTENT)
    except Exception as e:
        return {"error": str(e.args)}


@usuarios.post("/login", tags=["login"])
async def login(datos: Login):
    try:
        query = Usuarios.select().where(Usuarios.c.email == datos.email)
        user = db.execute(query).first()
        decr_data = checkPassword(datos.password, user[4])
        if len(user) > 0:
            if decr_data == True:
                return {
                    "success": True,
                    "user": user,
                }
            else:
                return {
                    "success": False,
                    "message": "Contraseña incorrecta"
                }
        else:
            return {
                "success": False,
                "message": "Usuario no existe"
            }
    except Exception as e:
        return {
            "success": False,
            "error": e
        }