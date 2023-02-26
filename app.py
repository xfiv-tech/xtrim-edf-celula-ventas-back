from fastapi import FastAPI, Request, HTTPException
from routes.usuario import usuarios
from routes.admin import administradores
from routes.edificio import edificios
from routes.reporte import reporte
from routes.roles import roles
from routes.menu import menu
from fastapi.middleware.cors import CORSMiddleware
import uuid
from dotenv import load_dotenv
import os
load_dotenv()

Token = os.getenv("Xtrim_token")

app = FastAPI(
    title="XTRIM API",
    description="A simple API to manage contacts",
    version="1.0.0",
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

# from fastapi import FastAPI

