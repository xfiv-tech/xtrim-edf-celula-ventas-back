from fastapi import FastAPI, Request, HTTPException
from routes.usuario import usuarios
from routes.admin import administradores
from routes.edificio import edificios
from routes.reporte import reporte
from fastapi.middleware.cors import CORSMiddleware
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

app.include_router(usuarios)
app.include_router(administradores)
app.include_router(edificios)
app.include_router(reporte)
# from fastapi import FastAPI

