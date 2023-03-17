import statistics
from middleware.validacionToken import ValidacionToken
from fastapi import APIRouter, Request, HTTPException, Response
from model.ModelSchema.channelModel import RegistrarAdminProyectosModel, RegistrarAdministradorModel, RegistrarDistribuidorModel, RegistrarGerenteCiudadModel, RegistrarGerenteModel, RegistrarGerenteRegionalModel, RegistrarJefeModel, RegistrarVendedorModel
from model.ModelSchema.menu import MenuBase, SubmenuBase
from model.channel import Channel, Ciudad, Estados, RegistrarAdminProyectos, RegistrarDistribuidor, RegistrarGerente, RegistrarGerenteCiudad, RegistrarGerenteRegional, RegistrarVendedor, RegistroAdministrador, RegistroJefeVentas
from model.menu import Menus
from model.submenu import Submenus
from database.db import db
from sqlalchemy import join, select, and_, or_, func, desc, asc

registro = APIRouter(route_class=ValidacionToken)

#lista de vendedores
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
        query = RegistrarVendedor.delete().where(
            RegistrarVendedor.id_registrar_vendedor == id_registrar_vendedor)
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
        query = RegistrarDistribuidor.join(
            Ciudad, Ciudad.c.id_ciudad == RegistrarDistribuidor.c.id_ciudad).join(
            Estados, Estados.c.id_estado == RegistrarDistribuidor.c.id_estado).select().with_only_columns([
                RegistrarDistribuidor.c.id_registrar_distribuidor,
                Ciudad.c.ciudad,
                Ciudad.c.id_ciudad,
                Ciudad.c.region,
                Estados.c.estado,
                Estados.c.id_estado,
                RegistrarDistribuidor.c.nombre_distribuidor,
                RegistrarDistribuidor.c.responsable,
                RegistrarDistribuidor.c.telefono,
                RegistrarDistribuidor.c.email,
                RegistrarDistribuidor.c.fecha_ingreso,
                RegistrarDistribuidor.c.fecha_salida
            ])       
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


@registro.delete("/eliminar_distribuidor/{id_registrar_distribuidor}", tags=["Distribuidor"])
async def delete_distribuidor(id_registrar_distribuidor: int):
    try:
        print (id_registrar_distribuidor)
        query = RegistrarDistribuidor.delete().where(
            RegistrarDistribuidor.c.id_registrar_distribuidor == id_registrar_distribuidor)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }


# Registrar Jefe de Venta
@registro.get("/listar_jefe_venta", tags=["Jefe de Venta"])
async def get_jefe_venta():
    try:
        query = RegistroJefeVentas.join(Channel, Channel.c.id_channel == RegistroJefeVentas.c.id_channel).join(
            Ciudad, Ciudad.c.id_ciudad == RegistroJefeVentas.c.id_ciudad).join(
            Estados, Estados.c.id_estado == RegistroJefeVentas.c.id_estado).select().with_only_columns([
                RegistroJefeVentas.c.id_jefe_venta,
                Channel.c.id_channel,
                Channel.c.channel,
                Ciudad.c.ciudad,
                Ciudad.c.id_ciudad,
                Ciudad.c.region,
                Estados.c.estado,
                Estados.c.id_estado,
                RegistroJefeVentas.c.nombre_jefe
            ])        
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


@registro.delete("/eliminar_jefe_venta/{id_jefe_venta}", tags=["Jefe de Venta"])
async def delete_jefe_venta(id_jefe_venta: int):
    try:
        query = RegistroJefeVentas.delete().where(
            RegistroJefeVentas.c.id_jefe_venta == id_jefe_venta)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }

# Registrar Administrador
@registro.get("/listar_administrador", tags=["Administrador"])
async def get_administrador():
    try:
        query = RegistroAdministrador.join(Channel, Channel.c.id_channel == RegistroAdministrador.c.id_channel).join(
            Ciudad, Ciudad.c.id_ciudad == RegistroAdministrador.c.id_ciudad).join(
            Estados, Estados.c.id_estado == RegistroAdministrador.c.id_estado).select().with_only_columns([
                RegistroAdministrador.c.id_administrador,
                Channel.c.id_channel,
                Channel.c.channel,
                Ciudad.c.ciudad,
                Ciudad.c.id_ciudad,
                Ciudad.c.region,
                Estados.c.estado,
                Estados.c.id_estado,
                RegistroAdministrador.c.nombre_administrador
            ])           
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
        query = RegistroAdministrador.delete().where(
            RegistroAdministrador.c.id_administrador == id_administrador)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }

# Registrar gerente
@registro.get("/listar_gerente", tags=["Gerente"])
async def get_gerente():
    try:
        query = RegistrarGerente.join(Channel, Channel.c.id_channel == RegistrarGerente.c.id_channel).join(
            Ciudad, Ciudad.c.id_ciudad == RegistrarGerente.c.id_ciudad).join(
            Estados, Estados.c.id_estado == RegistrarGerente.c.id_estado).select().with_only_columns([
                RegistrarGerente.c.id_gerente,
                Channel.c.id_channel,
                Channel.c.channel,
                Ciudad.c.ciudad,
                Ciudad.c.id_ciudad,
                Ciudad.c.region,
                Estados.c.estado,
                Estados.c.id_estado,
                RegistrarGerente.c.nombre_gerente
            ])
        print("Query", query)
        data = db.execute(query).fetchall()
        print("Data",data)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e.args)
        })


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


@registro.delete("/eliminar_gerente/{id_gerente}", tags=["Gerente"])
async def delete_gerente(id_gerente: int):
    try:
        query = RegistrarGerente.delete().where(
            RegistrarGerente.c.id_gerente == id_gerente)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }


# Registrar gerente regional
@registro.get("/listar_gerente_regional", tags=["Gerente Regional"])
async def get_gerente_ciudad():
    try:
        query = RegistrarGerenteRegional.join(Channel, Channel.c.id_channel == RegistrarGerenteRegional.c.id_channel).join(
            Ciudad, Ciudad.c.id_ciudad == RegistrarGerenteRegional.c.id_ciudad).join(
            Estados, Estados.c.id_estado == RegistrarGerenteRegional.c.id_estado).select().with_only_columns([
                RegistrarGerenteRegional.c.id_gerente_regional,
                Channel.c.id_channel,
                Channel.c.channel,
                Ciudad.c.ciudad,
                Ciudad.c.id_ciudad,
                Ciudad.c.region,
                Estados.c.estado,
                Estados.c.id_estado,
                RegistrarGerenteRegional.c.nombre_gerente
            ])
        data = db.execute(query).fetchall()
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {"error": str(e)}


@registro.post("/crear_gerente_regional", tags=["Gerente Regional"])
async def post_gerente_ciudad(request: RegistrarGerenteRegionalModel):
    try:
        query = RegistrarGerenteRegional.insert().values(
            id_gerente_regional=request.id_gerente_regional,
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


@registro.put("/actualizar_gerente_regional", tags=["Gerente Regional"])
async def put_gerente_ciudad(request: RegistrarGerenteRegionalModel):
    try:
        db.execute(RegistrarGerenteRegional.update().values(
            id_channel=request.id_channel,
            id_ciudad=request.id_ciudad,
            id_estado=request.id_estado,
            nombre_gerente_ciudad=request.nombre_gerente
        ).where(RegistrarGerenteRegional.c.id_gerente_regional == request.id_gerente_regional))
        return {
            "code": "0"
        }
    except Exception as e:
        return {"error": str(e)}


@registro.delete("/eliminar_gerente_regional/{id_gerente_regional}", tags=["Gerente Regional"])
async def delete_gerente_ciudad(id_gerente_regional: int):
    try:
        query = RegistrarGerenteRegional.delete().where(
            RegistrarGerenteRegional.c.id_gerente_regional == id_gerente_regional)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }


# Registrar gerente de ciudad
@registro.get("/listar_gerente_ciudad", tags=["Gerente de Ciudad"])
async def get_gerente_ciudad():
    try:
        query = RegistrarGerenteCiudad.join(Channel, Channel.c.id_channel == RegistrarGerenteCiudad.c.id_channel).join(
            Ciudad, Ciudad.c.id_ciudad == RegistrarGerenteCiudad.c.id_ciudad).join(
            Estados, Estados.c.id_estado == RegistrarGerenteCiudad.c.id_estado).select().with_only_columns([
                RegistrarGerenteCiudad.c.id_gerente_ciudad,
                Channel.c.id_channel,
                Channel.c.channel,
                Ciudad.c.ciudad,
                Ciudad.c.id_ciudad,
                Ciudad.c.region,
                Estados.c.estado,
                Estados.c.id_estado,
                RegistrarGerenteCiudad.c.nombre_gerente_ciudad
            ])
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


@registro.delete("/eliminar_gerente_ciudad/{id_gerente_ciudad}", tags=["Gerente de Ciudad"])
async def delete_gerente_ciudad(id_gerente_ciudad: int):
    try:
        query = RegistrarGerenteCiudad.delete().where(
            RegistrarGerenteCiudad.c.id_gerente_ciudad == id_gerente_ciudad)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }


# Administrador de proyectos

@registro.get("/listar_administrador_proyectos", tags=["Administrador de Proyectos"])
async def get_administrador_proyectos():
    try:
        query = RegistrarAdminProyectos.join(Channel, Channel.c.id_channel == RegistrarAdminProyectos.c.id_channel).join(
            Ciudad, Ciudad.c.id_ciudad == RegistrarAdminProyectos.c.id_ciudad).join(
            Estados, Estados.c.id_estado == RegistrarAdminProyectos.c.id_estado).select().with_only_columns([
                RegistrarAdminProyectos.c.id_admin_proyectos,
                Channel.c.id_channel,
                Channel.c.channel,
                Ciudad.c.ciudad,
                Ciudad.c.id_ciudad,
                Ciudad.c.region,
                Estados.c.estado,
                Estados.c.id_estado,
                RegistrarAdminProyectos.c.nombre_admin_proyectos
            ])        
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


@registro.delete("/eliminar_administrador_proyectos/{id_admin_proyectos}", tags=["Administrador de Proyectos"])
async def delete_administrador_proyectos(id_admin_proyectos: int):
    try:
        query = RegistrarAdminProyectos.delete().where(
            RegistrarAdminProyectos.c.id_admin_proyectos == id_admin_proyectos)
        data = db.execute(query)
        return {
            "code": "0",
            "data": data
        }
    except Exception as e:
        return {
            "error": str(e)
        }
