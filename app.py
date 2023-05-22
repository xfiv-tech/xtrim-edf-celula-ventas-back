from fastapi import FastAPI
from fastapi_scheduler import SchedulerAdmin
from routes.usuario import usuarios
from routes.admin import administradores
from routes.edificio import edificios
from routes.reporte import reporte
from routes.roles import roles
from routes.menu import menu
from routes.login import login
from routes.channel import channel
from routes.registroCelula import registro
from routes.asignacion import asignacion
from routes.codigo import codigo
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from task.reporte import tarea_programada

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

# app.include_router(usuarios,generate_unique_id_function=uuid.uuid1())
# app.include_router(administradores, generate_unique_id_function=uuid.uuid1())
# app.include_router(edificios, generate_unique_id_function=uuid.uuid1())
# app.include_router(reporte, generate_unique_id_function=uuid.uuid1())

# Create an instance of the scheduled task scheduler `SchedulerAdmin`
scheduler = SchedulerAdmin.scheduler

@scheduler.scheduled_job('interval', seconds=14400)
def interval_task_test():
    print('interval task is run...')
    tarea_programada()

# @scheduler.scheduled_job('cron', hour=3, minute=30)
# def cron_task_test():
#     print('cron task is run...')

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

@app.on_event("startup")
async def startup():
    # Mount the background management system
    scheduler.start()
# if DEV != "DEV":
#     os.system("python3 task/reporte.py")  
# from fastapi import FastAPI

