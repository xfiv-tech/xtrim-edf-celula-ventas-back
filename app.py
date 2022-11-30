from fastapi import FastAPI
from routes.usuario import usuarios
from routes.admin import administradores
from routes.edificio import edificios


app = FastAPI(
    title="XTRIM API",
    description="A simple API to manage contacts",
    version="1.0.0",
)

app.include_router(usuarios)
app.include_router(administradores)
app.include_router(edificios)