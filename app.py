from fastapi import FastAPI
from routes.usuario import usuarios
from routes.admin import administradores
from routes.edificio import edificios
from fastapi.middleware.cors import CORSMiddleware


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