from middleware.validacionToken import ValidacionToken
from fastapi import APIRouter, Request, HTTPException
from model.ModelSchema.menu import MenuBase, SubmenuBase
from model.menu import Menus
from model.submenu import Submenus
from database.db import db

registro = APIRouter(route_class=ValidacionToken)

@registro.get("/listar_registro", tags=["Celula"])
# async def get_registro():


