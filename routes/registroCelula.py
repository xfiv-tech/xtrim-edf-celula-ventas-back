from middleware.validacionToken import ValidacionToken
from fastapi import APIRouter, Request, HTTPException
from model.ModelSchema.channelModel import RegistrarVendedorModel
from model.ModelSchema.menu import MenuBase, SubmenuBase
from model.channel import RegistrarVendedor
from model.menu import Menus
from model.submenu import Submenus
from database.db import db

registro = APIRouter(route_class=ValidacionToken)

@registro.get("/listar_registro", tags=["Vendedor"])
async def get_registro():
    try:
        query = RegistrarVendedor.select()
        data = db.execute(query).fetchall()
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}


@registro.post("/crear_registro", tags=["Vendedor"])
async def post_registro(request: RegistrarVendedorModel):
    try:
        query = RegistrarVendedor.insert().values(
            id_channel=request.id_channel,
            id_mando=request.id_mando,
            id_ciudad=request.id_ciudad,
            id_operador=request.id_operador,
            id_sistema_operativo=request.id_sistema_operativo,
            id_estado=request.id_estado,
            id_genero=request.id_genero,
            id_modalidad=request.id_modalidad,
            cedula=request.cedula,
            codigo_vendedor=request.codigo_vendedor,
            usuario_equifax=request.usuario_equifax,
            nombre_vendedor=request.nombre_vendedor,
            fecha_ingreso=request.fecha_ingreso,
            id_gerente=request.id_gerente,
            id_gerente_ciudad=request.id_gerente_ciudad,
            id_jefe_venta=request.id_jefe_venta,
            id_lider_peloton=request.id_lider_peloton,
            ciudad_gestion=request.ciudad_gestion,
            lider_check=request.lider_check,
            meta_volumen=request.meta_volumen,
            meta_dolares=request.meta_dolares,
            fecha_salida=request.fecha_salida,
            sector_residencia=request.sector_residencia,
            email=request.email
            cedula=request.cedula,
            dias_inactivo=request.dias_inactivo
        )
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}

@registro.put("/actualizar_registro", tags=["Vendedor"])
async def put_registro(request: RegistrarVendedorModel):
    try:
        query = RegistrarVendedor.update().values(
            id_channel=request.id_channel,
            id_mando=request.id_mando,
            id_ciudad=request.id_ciudad,
            id_operador=request.id_operador,
            id_sistema_operativo=request.id_sistema_operativo,
            id_estado=request.id_estado,
            id_genero=request.id_genero,
            id_modalidad=request.id_modalidad,
            cedula=request.cedula,
            codigo_vendedor=request.codigo_vendedor,
            usuario_equifax=request.usuario_equifax,
            nombre_vendedor=request.nombre_vendedor,
            fecha_ingreso=request.fecha_ingreso,
            id_gerente=request.id_gerente,
            id_gerente_ciudad=request.id_gerente_ciudad,
            id_jefe_venta=request.id_jefe_venta,
            id_lider_peloton=request.id_lider_peloton,
            ciudad_gestion=request.ciudad_gestion,
            lider_check=request.lider_check,
            meta_volumen=request.meta_volumen,
            meta_dolares=request.meta_dolares,
            fecha_salida=request.fecha_salida,
            sector_residencia=request.sector_residencia,
            email=request.email,
            cedula=request.cedula,
            dias_inactivo=request.dias_inactivo
        ).where(RegistrarVendedor.c.id_registrar_vendedor == request.id_registrar_vendedor)
        return {
            "code": "0",
            "data": query
        }
    except Exception as e:
        return {"error": str(e)}

    
@registro.delete("/eliminar_registro", tags=["Vendedor"])
async def delete_registro(request: RegistrarVendedorModel):
    try:
        query = RegistrarVendedor.delete().where(RegistrarVendedor.id_registrar_vendedor == request.id_registrar_vendedor)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }