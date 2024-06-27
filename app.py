import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from routes.admin import administradores
from routes.asignacion import asignacion
from routes.channel import channel
from routes.codigo import codigo
from routes.edificio import edificios
from routes.isla import isla
from routes.login import login
from routes.menu import menu
from routes.planform import planform
from routes.registroCelula import registro
from routes.reporte import reporte
from routes.roles import roles
from routes.usuario import usuarios
from routes.Zonal import zonal
from task.reporte import tarea_Inicial, tarea_programada

load_dotenv()

Token = os.getenv("Xtrim_token")
DEV = os.getenv("DEV")

app = FastAPI(
    title="XTRIM API",
    description="A simple API to manage contacts",
    version="1.0.0",
    root_path="/back_celula_prod" if DEV == "PRO" else "/",
    root_path_in_servers=True,
    authorizations={

    }
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def startup():
    print("Starting up...")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(tarea_programada, CronTrigger(
        hour=17, minute=42), id="tarea_programada")
    scheduler.start()


@app.on_event("shutdown")
async def shutdown():
    print("Shutting down...")
    scheduler.shutdown()
    print("Shutdown complete")

app.include_router(usuarios)
app.include_router(administradores)
app.include_router(edificios)
app.include_router(reporte)
app.include_router(roles)
app.include_router(menu)
app.include_router(login)
app.include_router(registro)
app.include_router(channel)
app.include_router(asignacion)
app.include_router(codigo)
app.include_router(isla)
app.include_router(zonal)
app.include_router(planform)
