


from MigrationPy.migration import RegistrarGerenteCiudad, RegistrarGerenteRegional, RegistrarVendedor, RegistroJefeVentas
from controller.AsignacionController import ListarCiudadesAPCiudad
from database.db import db
from model.channel import RegistrarAdminProyectos


async def SelectAdminProyectCiudad(id_ciudad:int):
    try:
        nombre_admin_proyect = RegistrarAdminProyectos.select()
        admin_proyect = db.execute(nombre_admin_proyect).fetchall()
        infoData = []
        for i in admin_proyect:
            response = await ListarCiudadesAPCiudad(i["id_admin_proyectos"])
            if response != None:
                for j in response:
                    if j["id_ciudad"] == id_ciudad:
                        infoData.append({
                            "id_admin_proyectos": i["id_admin_proyectos"],
                            "nombre_admin_proyectos": i["nombre_admin_proyectos"],
                        })
                        return infoData[0]["nombre_admin_proyectos"]

        return infoData[0]["nombre_admin_proyectos"]
    except Exception as e:
        print(e)
        return None
    

async def SelectLiderPeloton(id_lider_peloton:int):
    try:
        if id_lider_peloton == None or id_lider_peloton == 0:
            return "NO APLICA"
        nombre_lider = RegistrarVendedor.select().where(RegistrarVendedor.c.id_lider_peloton == id_lider_peloton)
        query = db.execute(nombre_lider).fetchall()
        for i in query:
            if i["id_admin_proyectos"] == id_lider_peloton:
                return i["nombre_vendedor"]
    except Exception as e:
        print(e)
        return "NO APLICA"
    

async def SelectJefeVenta(id_jefe_venta:int):
    try:
        if id_jefe_venta == None or id_jefe_venta == 0:
            return "SIN JEFE VENTA"
        nombre_jefe = RegistroJefeVentas.select().where(RegistroJefeVentas.c.id_jefe_venta == id_jefe_venta)
        query = db.execute(nombre_jefe).fetchall()
        for i in query:
                return i["nombre_jefe"]
    except Exception as e:
        print(e)
        return "SIN JEFE VENTA"
    

async def SelectGerenteCiudad(id_gerente_ciudad:int):
    try:
        if id_gerente_ciudad == None or id_gerente_ciudad == 0:
            return "SIN GERENTE CIUDAD"
        nombre_gerente = RegistrarGerenteCiudad.select().where(RegistrarGerenteCiudad.c.id_gerente_ciudad == id_gerente_ciudad)
        query = db.execute(nombre_gerente).fetchall()
        for i in query:
                return i["nombre_gerente_ciudad"]
    except Exception as e:
        print(e)
        return "SIN GERENTE CIUDAD"
    

async def SelectGerenteRegional(id_gerente_regional:int):
    try:
        if id_gerente_regional == None or id_gerente_regional == 0:
            return "SIN GERENTE REGIONAL"
        nombre_gerente = RegistrarGerenteRegional.select().where(RegistrarGerenteRegional.c.id_gerente_regional == id_gerente_regional)
        query = db.execute(nombre_gerente).fetchall()
        for i in query:
                return i["nombre_gerente"]
    except Exception as e:
        print(e)
        return "SIN GERENTE REGIONAL"