from fastapi import FastAPI, Request, HTTPException
from middleware.validacionToken import ValidacionToken
from routes.usuario import usuarios
from routes.admin import administradores
from routes.edificio import edificios
from routes.reporte import reporte
from routes.roles import roles
from routes.menu import menu
from routes.login import login
from routes.channel import channel
from routes.registroCelula import registro

from fastapi.middleware.cors import CORSMiddleware
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

Token = os.getenv("Xtrim_token")
DEV = os.getenv("DEV")

app = FastAPI(
    title="XTRIM API",
    description="A simple API to manage contacts",
    version="1.0.0",
    # openapi_prefix="/back_edificios_dev",
    #"https://incoming.xfiv.chat/whatsapp_cloud/api/v1/send/message" if PLATAFORMA == "DEV" != None else conversacion["data"]["path_conector"]
    root_path="/back_edificios_dev" if DEV == "PRO" else "/",
    root_path_in_servers=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(usuarios,generate_unique_id_function=uuid.uuid1())
# app.include_router(administradores, generate_unique_id_function=uuid.uuid1())
# app.include_router(edificios, generate_unique_id_function=uuid.uuid1())
# app.include_router(reporte, generate_unique_id_function=uuid.uuid1())

app.include_router(usuarios)
app.include_router(administradores)
app.include_router(edificios)
app.include_router(reporte)
app.include_router(roles)
app.include_router(menu)
app.include_router(login)
app.include_router(channel)
app.include_router(registro)

# from fastapi import FastAPI

