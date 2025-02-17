from controller.AsignacionController import ListarCiudadesAPCiudad
from database.db import db
from model.channel import (
    Channel,
    RegistrarAdminProyectos,
    RegistrarDistribuidor,
    RegistrarGerenteCiudad,
    RegistrarGerenteRegional,
    RegistrarGerenteZonal,
    RegistrarVendedor,
    RegistroJefeVentas,
)


async def SelectAdminProyectCiudad(id_ciudad: int):
    try:
        nombre_admin_proyect = RegistrarAdminProyectos.select()
        result = db.execute(nombre_admin_proyect).fetchall()
        admin_proyect = [dict(row._mapping) for row in result]

        infoData = []
        for i in admin_proyect:
            response = await ListarCiudadesAPCiudad(i["id_admin_proyectos"])
            if response != None:
                for j in response:
                    if j["id_ciudad"] == id_ciudad:
                        infoData.append(
                            {
                                "id_admin_proyectos": i["id_admin_proyectos"],
                                "nombre_admin_proyectos": i["nombre_admin_proyectos"],
                            }
                        )
                        return infoData[0]["nombre_admin_proyectos"]

        return infoData[0]["nombre_admin_proyectos"]
    except Exception as e:
        print(e)
        return None


async def SelectLiderPeloton(id_lider_peloton: int, id_channel: int):
    try:
        if id_lider_peloton == None or id_lider_peloton == 0:
            return "NO APLICA"

        # sacar el nombre del canal
        if id_channel == None or id_channel == 0:
            return "NO APLICA"

        if id_channel == 1 or id_channel == 4 or id_channel == 5:
            nombre_lider = RegistrarDistribuidor.select().where(
                RegistrarDistribuidor.c.id_registrar_distribuidor == id_lider_peloton
            )
            result = db.execute(nombre_lider).fetchall()
            query = [dict(row._mapping) for row in result]
            for i in query:
                return i["nombre_distribuidor"]

        nombre_lider = RegistrarVendedor.select().where(
            RegistrarVendedor.c.id_registrar_vendedor == id_lider_peloton
        )
        query = db.execute(nombre_lider).fetchall()
        for i in query:
            return i["nombre_vendedor"]
    except Exception as e:
        return "NO APLICA"


async def SelectJefeVenta(id_jefe_venta: int):
    try:
        if id_jefe_venta == None or id_jefe_venta == 0:
            return "SIN JEFE VENTA"
        nombre_jefe = RegistroJefeVentas.select().where(
            RegistroJefeVentas.c.id_jefe_venta == id_jefe_venta
        )
        result = db.execute(nombre_jefe).fetchall()
        query = [dict(row._mapping) for row in result]
        for i in query:
            return i["nombre_jefe"]
    except Exception as e:
        print(e)
        return "SIN JEFE VENTA"


async def SelectGerenteCiudad(id_gerente_ciudad: int):
    try:
        if id_gerente_ciudad == None or id_gerente_ciudad == 0:
            return "SIN GERENTE CIUDAD"
        nombre_gerente = RegistrarGerenteCiudad.select().where(
            RegistrarGerenteCiudad.c.id_gerente_ciudad == id_gerente_ciudad
        )
        result = db.execute(nombre_gerente).fetchall()
        query = [dict(row._mapping) for row in result]
        for i in query:
            return i["nombre_gerente_ciudad"]
    except Exception as e:
        print(e)
        return "SIN GERENTE CIUDAD"


async def SelectGerenteRegional(id_gerente_regional: int):
    try:
        if id_gerente_regional == None or id_gerente_regional == 0:
            return "SIN GERENTE REGIONAL"
        nombre_gerente = RegistrarGerenteRegional.select().where(
            RegistrarGerenteRegional.c.id_gerente_regional == id_gerente_regional
        )
        result = db.execute(nombre_gerente).fetchall()
        query = [dict(row._mapping) for row in result]
        for i in query:
            return i["nombre_gerente"]
    except Exception as e:
        print(e)
        return "SIN GERENTE REGIONAL"


async def ZonalIdGerente(id: int):
    try:
        # print("ZonalIdGerente: ", id)
        if id == None or id == 0:
            return "SIN GERENTE ZONAL"
        result = db.execute(
            RegistrarGerenteZonal.select().where(
                RegistrarGerenteZonal.c.id_gerente_zonal == id
            )
        ).fetchall()
        query = [dict(row._mapping) for row in result]
        if len(query) > 0:
            return query[0]["nombre"]
        return "SIN GERENTE ZONAL"
    except Exception as e:
        print(e.args)
        return "SIN GERENTE ZONAL"


async def ZonalGerente():
    try:
        info = []
        result = db.execute(RegistrarGerenteZonal.select()).fetchall()
        query = [dict(row._mapping) for row in result]
        if len(query) > 0:
            for i in query:
                info.append(
                    {"id_gerente_zonal": i["id_gerente_zonal"], "nombre": i["nombre"]}
                )
            return info
        return "SIN GERENTE ZONAL"
    except Exception as e:
        print(e.args)
        return "SIN GERENTE ZONAL"
