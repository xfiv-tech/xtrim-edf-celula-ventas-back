from middleware.validacionToken import ValidacionToken
from fastapi import APIRouter, Request, HTTPException
from model.ModelSchema.channelModel import RegistrarAdminProyectosModel, RegistrarAdministradorModel, RegistrarDistribuidorModel, RegistrarGerenteCiudadModel, RegistrarGerenteModel, RegistrarJefeModel, RegistrarVendedorModel
from model.ModelSchema.menu import MenuBase, SubmenuBase
from model.channel import RegistrarAdminProyectos, RegistrarDistribuidor, RegistrarGerente, RegistrarGerenteCiudad, RegistrarVendedor, RegistroAdministrador, RegistroJefeVentas
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
            email=request.email,
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
            dias_inactivo=request.dias_inactivo
        ).where(RegistrarVendedor.c.id_registrar_vendedor == request.id_registrar_vendedor)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}

    
@registro.delete("/eliminar_registro", tags=["Vendedor"])
async def delete_registro(id_registrar_vendedor: int):
    try:
        query = RegistrarVendedor.delete().where(RegistrarVendedor.id_registrar_vendedor == id_registrar_vendedor)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }
    

# Reistrar Distribuidor
@registro.get("/listar_distribuidor", tags=["Distribuidor"])
async def get_distribuidor():
    try:
        query = RegistrarDistribuidor.select()
        data = db.execute(query).fetchall()
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}

@registro.post("/crear_distribuidor", tags=["Distribuidor"])
async def post_distribuidor(request: RegistrarDistribuidorModel):
    try:
        query = RegistrarDistribuidor.insert().values(
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_distribuidor=request.nombre_distribuidor,
            responsable=request.responsable,
            telefono=request.telefono,
            email=request.email,
            fecha_ingreso=request.fecha_ingreso,
            fecha_salida=request.fecha_salida
        )
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}
    

@registro.put("/actualizar_distribuidor", tags=["Distribuidor"])
async def put_distribuidor(request: RegistrarDistribuidorModel):
    try:
        query = RegistrarDistribuidor.update().values(
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_distribuidor=request.nombre_distribuidor,
            responsable=request.responsable,
            telefono=request.telefono,
            email=request.email,
            fecha_ingreso=request.fecha_ingreso,
            fecha_salida=request.fecha_salida
        ).where(RegistrarDistribuidor.c.id_registrar_distribuidor == request.id_registrar_distribuidor)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}
    

@registro.delete("/eliminar_distribuidor", tags=["Distribuidor"])
async def delete_distribuidor(id_registrar_distribuidor: int):
    try:
        query = RegistrarDistribuidor.delete().where(RegistrarDistribuidor.id_registrar_distribuidor == id_registrar_distribuidor)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }


#Registrar Jefe de Venta
@registro.get("/listar_jefe_venta", tags=["Jefe de Venta"])
async def get_jefe_venta():
    try:
        query = RegistroJefeVentas.select()
        data = db.execute(query).fetchall()
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}


@registro.post("/crear_jefe_venta", tags=["Jefe de Venta"])
async def post_jefe_venta(request: RegistrarJefeModel):
    try:
        query = RegistroJefeVentas.insert().values(
            id_jefe_venta=request.id_jefe_venta,
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            nombre_jefe=request.nombre_jefe
        )
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}
    

@registro.put("/actualizar_jefe_venta", tags=["Jefe de Venta"])
async def put_jefe_venta(request: RegistrarJefeModel):
    try:
        query = RegistroJefeVentas.update().values(
            id_jefe_venta=request.id_jefe_venta,
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            nombre_jefe=request.nombre_jefe
        ).where(RegistroJefeVentas.c.id_jefe_venta == request.id_jefe_venta)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}
    

@registro.delete("/eliminar_jefe_venta", tags=["Jefe de Venta"])
async def delete_jefe_venta(id_jefe_venta: int):
    try:
        query = RegistroJefeVentas.delete().where(RegistroJefeVentas.id_jefe_venta == id_jefe_venta)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }
    
#Registrar Administrador
@registro.get("/listar_administrador", tags=["Administrador"])
async def get_administrador():
    try:
        query = RegistroAdministrador.select()
        data = db.execute(query).fetchall()
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}


@registro.post("/crear_administrador", tags=["Administrador"])
async def post_administrador(request: RegistrarAdministradorModel):
    try:
        query = RegistroAdministrador.insert().values(
            id_administrador=request.id_administrador,
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_administrador=request.nombre_administrador
        )
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}
    

@registro.put("/actualizar_administrador", tags=["Administrador"])
async def put_administrador(request: RegistrarAdministradorModel):
    try:
        data = db.execute(RegistroAdministrador.update().values(
            id_administrador=request.id_administrador,
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_administrador=request.nombre_administrador
        ).where(RegistroAdministrador.c.id_administrador == request.id_administrador))
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}
    

@registro.delete("/eliminar_administrador", tags=["Administrador"])
async def delete_administrador(id_administrador: int):
    try:
        query = RegistroAdministrador.delete().where(RegistroAdministrador.id_administrador == id_administrador)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }
    
#Registrar gerente
@registro.get("/listar_gerente", tags=["Gerente"])
async def get_gerente():
    try:
        query = RegistrarGerente.select()
        data = db.execute(query).fetchall()
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}
    

@registro.post("/crear_gerente", tags=["Gerente"])
async def post_gerente(request: RegistrarGerenteModel):
    try:
        query = RegistrarGerente.insert().values(
            id_gerente=request.id_gerente,
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_gerente=request.nombre_gerente
        )
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}
    

@registro.put("/actualizar_gerente", tags=["Gerente"])
async def put_gerente(request: RegistrarGerenteModel):
    try:
        data = db.execute(RegistrarGerente.update().values(
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_gerente=request.nombre_gerente
        ).where(RegistrarGerente.c.id_gerente == request.id_gerente))
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}
    

@registro.delete("/eliminar_gerente", tags=["Gerente"])
async def delete_gerente(id_gerente: int):
    try:
        query = RegistrarGerente.delete().where(RegistrarGerente.id_gerente == id_gerente)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }
    

#Registrar gerente de ciudad
@registro.get("/listar_gerente_ciudad", tags=["Gerente de Ciudad"])
async def get_gerente_ciudad():
    try:
        query = RegistrarGerenteCiudad.select()
        data = db.execute(query).fetchall()
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}
    
@registro.post("/crear_gerente_ciudad", tags=["Gerente de Ciudad"])
async def post_gerente_ciudad(request: RegistrarGerenteCiudadModel):
    try:
        query = RegistrarGerenteCiudad.insert().values(
            id_gerente_ciudad=request.id_gerente_ciudad,
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_gerente_ciudad=request.nombre_gerente_ciudad
        )
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}
    

@registro.put("/actualizar_gerente_ciudad", tags=["Gerente de Ciudad"])
async def put_gerente_ciudad(request: RegistrarGerenteCiudadModel):
    try:
        db.execute(RegistrarGerenteCiudad.update().values(
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_gerente_ciudad=request.nombre_gerente_ciudad
        ).where(RegistrarGerenteCiudad.c.id_gerente_ciudad == request.id_gerente_ciudad))
        return {
            "code": "0"
        }
    except Exception as e:
        return {"error": str(e)}
    

@registro.delete("/eliminar_gerente_ciudad", tags=["Gerente de Ciudad"])
async def delete_gerente_ciudad(id_gerente_ciudad: int):
    try:
        query = RegistrarGerenteCiudad.delete().where(RegistrarGerenteCiudad.id_gerente_ciudad == id_gerente_ciudad)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }
    

#Administrador de proyectos

@registro.get("/listar_administrador_proyectos", tags=["Administrador de Proyectos"])
async def get_administrador_proyectos():
    try:
        query = RegistrarAdminProyectos.select()
        data = db.execute(query).fetchall()
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}
    

@registro.post("/crear_administrador_proyectos", tags=["Administrador de Proyectos"])
async def post_administrador_proyectos(request: RegistrarAdminProyectosModel):
    try:
        query = RegistrarAdminProyectos.insert().values(
            id_admin_proyectos=request.id_admin_proyectos,
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_admin_proyectos=request.nombre_admin_proyectos
        )
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}
    

@registro.put("/actualizar_administrador_proyectos", tags=["Administrador de Proyectos"])
async def put_administrador_proyectos(request: RegistrarAdminProyectosModel):
    try:
        data = db.execute(RegistrarAdminProyectos.update().values(
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_admin_proyectos=request.nombre_admin_proyectos
        ).where(RegistrarAdminProyectos.c.id_admin_proyectos == request.id_admin_proyectos))
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}
    

@registro.delete("/eliminar_administrador_proyectos", tags=["Administrador de Proyectos"])
async def delete_administrador_proyectos(id_admin_proyectos: int):
    try:
        query = RegistrarAdminProyectos.delete().where(RegistrarAdminProyectos.id_admin_proyectos == id_admin_proyectos)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }