


from model.ModelSchema.asignacionModel import ArrayAsigancionCanalAdmin, ArrayAsigancionCanalDistribuidor, ArrayAsigancionCanalGciudad, ArrayAsigancionCanalGregional, ArrayAsigancionCanalJefe, ArrayAsigancionCiudadAdmin, ArrayAsigancionCiudadDistribuidor, ArrayAsigancionCiudadGciudad, ArrayAsigancionCiudadGreginal, ArrayAsigancionCiudadJefe
from model.channel import Channel, Ciudad, asignacion_ciudades_gerente_regional, asiganacion_canal_gerente_regional
from model.channel import asignacion_ciudades_gerente_ciudad,asignacion_canal_gerente_ciudad
from model.channel import asignacion_ciudades_jefe_ventas,asignacion_canal_jefe_ventas
from model.channel import asignacion_ciudades_admin_proyectos,asignacion_canal_admin_proyectos
from model.channel import asignacion_ciudades_distribuidor,asignacion_canal_distribuidor


from database.db import db
#Gerente regional
async def AsignarCiudadesGRegional(data: ArrayAsigancionCiudadGreginal):
    try:
        for i in data.data:
            if i.id_gerente_ciudad != 0 and i.id_ciudad != 0:
                query = asignacion_ciudades_gerente_regional.insert().values(
                    id_ciudad=i.id_ciudad,
                    id_gerente_regional=i.id_gerente_regional,
                )
                db.execute(query)
        return {"status": 200, "message": "Asignacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def ListarCiudadesGRegional(id_gerente_regional: int):
    try:
        query = asignacion_ciudades_gerente_regional.join(Channel, asiganacion_canal_gerente_regional.c.id_ciudad == Ciudad.c.id_ciudad).select().where(
            asignacion_ciudades_gerente_regional.c.id_gerente_regional == id_gerente_regional
        )
        return db.execute(query).fetchall()
    except Exception as e:
        return {"status": 400, "message": str(e)}

async def DeleteCiudadesGRegional(id_asignacion_ciudades: int):
    try:
        query = asignacion_ciudades_gerente_regional.delete().where(
            asignacion_ciudades_gerente_regional.c.id_asignacion_ciudades == id_asignacion_ciudades
        )
        db.execute(query)
        return {"status": 200, "message": "Eliminacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    

async def AsignarCanalesGRciudad(data: ArrayAsigancionCanalGregional):
    try:
        for i in data.data:
            if i.id_channel != 0 and i.id_gerente_regional != 0:
                query = asiganacion_canal_gerente_regional.insert().values(
                    id_channel=i.id_channel,
                    id_gerente_regional=i.id_gerente_regional,
                )
                db.execute(query)
        return {"status": 200, "message": "Asignacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def ListarCanalesGRciudad(id_gerente_regional: int):
    try:
        query = asiganacion_canal_gerente_regional.join(Channel, asiganacion_canal_gerente_regional.c.id_channel == Channel.c.id_channel).select().where(
            asiganacion_canal_gerente_regional.c.id_gerente_regional == id_gerente_regional
        )
        return db.execute(query).fetchall()
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def DeleteCanalesGRciudad(id_asignacion_canal: int):
    try:
        query = asiganacion_canal_gerente_regional.delete().where(
            asiganacion_canal_gerente_regional.c.id_asignacion_canal == id_asignacion_canal
        )
        db.execute(query)
        return {"status": 200, "message": "Eliminacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    

#Gerente ciudad
async def AsignarCiudadesGCiudad(data: ArrayAsigancionCiudadGciudad):
    try:
        for i in data.data:
            if i.id_gerente_ciudad != 0 and i.id_ciudad != 0:
                query = asignacion_ciudades_gerente_ciudad.insert().values(
                    id_ciudad=i.id_ciudad,
                    id_gerente_ciudad=i.id_gerente_ciudad,
                )
                db.execute(query)
        return {"status": 200, "message": "Asignacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}

async def ListarCiudadesGCiudad(id_gerente_ciudad: int):
    try:
        query = asignacion_ciudades_gerente_ciudad.join(Channel, asignacion_ciudades_gerente_ciudad.c.id_ciudad == Ciudad.c.id_ciudad).select().where(
            asignacion_ciudades_gerente_ciudad.c.id_gerente_ciudad == id_gerente_ciudad
        )
        return db.execute(query).fetchall()
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def DeleteCiudadesGCiudad(id_asignacion_ciudades_gerente_ciudad: int):
    try:
        query = asignacion_ciudades_gerente_ciudad.delete().where(
            asignacion_ciudades_gerente_ciudad.c.id_asignacion_ciudades_gerente_ciudad == id_asignacion_ciudades_gerente_ciudad
        )
        db.execute(query)
        return {"status": 200, "message": "Eliminacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def AsignarCanalesGCiudad(data: ArrayAsigancionCanalGciudad):
    try:
        for i in data.data:
            if i.id_channel != 0 and i.id_gerente_ciudad != 0:
                query = asignacion_canal_gerente_ciudad.insert().values(
                    id_channel=i.id_channel,
                    id_gerente_ciudad=i.id_gerente_ciudad,
                )
                db.execute(query)
        return {"status": 200, "message": "Asignacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def ListarCanalesGCiudad(id_gerente_ciudad: int):
    try:
        query = asignacion_canal_gerente_ciudad.join(Channel, asignacion_canal_gerente_ciudad.c.id_channel == Channel.c.id_channel).select().where(
            asignacion_canal_gerente_ciudad.c.id_gerente_ciudad == id_gerente_ciudad
        )
        return db.execute(query).fetchall()
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def DeleteCanalesGCiudad(id_asignacion_canal_gerente_ciudad: int):
    try:
        query = asignacion_canal_gerente_ciudad.delete().where(
            asignacion_canal_gerente_ciudad.c.id_asignacion_canal_gerente_ciudad == id_asignacion_canal_gerente_ciudad
        )
        db.execute(query)
        return {"status": 200, "message": "Eliminacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
#Jefe de venta
async def AsignarCiudadesJVCiudad(data: ArrayAsigancionCiudadJefe):
    try:
        for i in data.data:
            if i.id_jefe_venta != 0 and i.id_ciudad != 0:
                query = asignacion_ciudades_jefe_ventas.insert().values(
                    id_ciudad=i.id_ciudad,
                    id_jefe_venta=i.id_jefe_venta,
                )
                db.execute(query)
        return {"status": 200, "message": "Asignacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def ListarCiudadesJVCiudad(id_jefe_venta: int):
    try:
        query = asignacion_ciudades_jefe_ventas.join(Ciudad, asignacion_ciudades_jefe_ventas.c.id_ciudad == Ciudad.c.id_ciudad).select().where(
            asignacion_ciudades_jefe_ventas.c.id_jefe_venta == id_jefe_venta
        )
        return db.execute(query).fetchall()
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def DeleteCiudadesJVCiudad(id_asignacion_ciudades_jefe_ventas: int):
    try:
        query = asignacion_ciudades_jefe_ventas.delete().where(
            asignacion_ciudades_jefe_ventas.c.id_asignacion_ciudades_jefe_ventas == id_asignacion_ciudades_jefe_ventas
        )
        db.execute(query)
        return {"status": 200, "message": "Eliminacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def AsignarCanalesJVCiudad(data: ArrayAsigancionCanalJefe):
    try:
        for i in data.data:
            if i.id_channel != 0 and i.id_jefe_venta != 0:
                query = asignacion_canal_jefe_ventas.insert().values(
                    id_channel=i.id_channel,
                    id_jefe_venta=i.id_jefe_venta,
                )
                db.execute(query)
        return {"status": 200, "message": "Asignacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def ListarCanalesJVCiudad(id_jefe_venta: int):
    try:
        query = asignacion_canal_jefe_ventas.join(Channel, asignacion_canal_jefe_ventas.c.id_channel == Channel.c.id_channel).select().where(
            asignacion_canal_jefe_ventas.c.id_jefe_venta == id_jefe_venta
        )
        return db.execute(query).fetchall()
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def DeleteCanalesJVCiudad(id_asignacion_canal_jefe_ventas: int):
    try:
        query = asignacion_canal_jefe_ventas.delete().where(
            asignacion_canal_jefe_ventas.c.id_asignacion_canal_jefe_ventas == id_asignacion_canal_jefe_ventas
        )
        db.execute(query)
        return {"status": 200, "message": "Eliminacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    

#Administrador Proyecto
async def AsignarCiudadesAPCiudad(data: ArrayAsigancionCiudadAdmin):
    try:
        for i in data.data:
            if i.id_admin_proyecto != 0 and i.id_ciudad != 0:
                query = asignacion_ciudades_admin_proyectos.insert().values(
                    id_ciudad=i.id_ciudad,
                    id_admin_proyecto=i.id_admin_proyecto,
                )
                db.execute(query)
        return {"status": 200, "message": "Asignacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}

async def ListarCiudadesAPCiudad(id_admin_proyecto: int):
    try:
        query = asignacion_ciudades_admin_proyectos.join(Ciudad, asignacion_ciudades_admin_proyectos.c.id_ciudad == Ciudad.c.id_ciudad).select().where(
            asignacion_ciudades_admin_proyectos.c.id_admin_proyecto == id_admin_proyecto
        )
        return db.execute(query).fetchall()
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def DeleteCiudadesAPCiudad(id_admin_proyecto: int):
    try:
        query = asignacion_ciudades_admin_proyectos.delete().where(
            asignacion_ciudades_admin_proyectos.c.id_admin_proyecto == id_admin_proyecto
        )
        db.execute(query)
        return {"status": 200, "message": "Eliminacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def AsignarCanalesAPCiudad(data: ArrayAsigancionCanalAdmin):
    try:
        for i in data.data:
            if i.id_channel != 0 and i.id_admin_proyecto != 0:
                query = asignacion_canal_admin_proyectos.insert().values(
                    id_channel=i.id_channel,
                    id_admin_proyecto=i.id_admin_proyecto,
                )
                db.execute(query)
        return {"status": 200, "message": "Asignacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def ListarCanalesAPCiudad(id_admin_proyecto: int):
    try:
        query = asignacion_canal_admin_proyectos.join(Channel, asignacion_canal_admin_proyectos.c.id_channel == Channel.c.id_channel).select().where(
            asignacion_canal_admin_proyectos.c.id_admin_proyecto == id_admin_proyecto
        )
        return db.execute(query).fetchall()
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def DeleteCanalesAPCiudad(id_admin_proyecto: int):
    try:
        query = asignacion_canal_admin_proyectos.delete().where(
            asignacion_canal_admin_proyectos.c.id_admin_proyecto == id_admin_proyecto
        )
        db.execute(query)
        return {"status": 200, "message": "Eliminacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
#Distribuidor
async def AsignarCiudadesDistribuidor(data: ArrayAsigancionCiudadDistribuidor):
    try:
        for i in data.data:
            if i.id_distribuidor != 0 and i.id_ciudad != 0:
                query = asignacion_ciudades_distribuidor.insert().values(
                    id_ciudad=i.id_ciudad,
                    id_distribuidor=i.id_distribuidor,
                )
                db.execute(query)
        return {"status": 200, "message": "Asignacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def ListarCiudadesDistribuidor(id_distribuidor: int):
    try:
        query = asignacion_ciudades_distribuidor.join(Ciudad, asignacion_ciudades_distribuidor.c.id_ciudad == Ciudad.c.id_ciudad).select().where(
            asignacion_ciudades_distribuidor.c.id_distribuidor == id_distribuidor
        )
        return db.execute(query).fetchall()
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def DeleteCiudadesDistribuidor(id_asignacion_ciudades_distribuidor: int):
    try:
        query = asignacion_ciudades_distribuidor.delete().where(
            asignacion_ciudades_distribuidor.c.id_asignacion_ciudades_distribuidor == id_asignacion_ciudades_distribuidor
        )
        db.execute(query)
        return {"status": 200, "message": "Eliminacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def AsignarCanalesDistribuidor(data: ArrayAsigancionCanalDistribuidor):
    try:
        for i in data.data:
            if i.id_channel != 0 and i.id_distribuidor != 0:
                query = asignacion_canal_distribuidor.insert().values(
                    id_channel=i.id_channel,
                    id_distribuidor=i.id_distribuidor,
                )
                db.execute(query)
        return {"status": 200, "message": "Asignacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def ListarCanalesDistribuidor(id_distribuidor: int):
    try:
        query = asignacion_canal_distribuidor.join(Channel, asignacion_canal_distribuidor.c.id_channel == Channel.c.id_channel).select().where(
            asignacion_canal_distribuidor.c.id_distribuidor == id_distribuidor
        )
        return db.execute(query).fetchall()
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def DeleteCanalesDistribuidor(id_asignacion_canal_distribuidor: int):
    try:
        query = asignacion_canal_distribuidor.delete().where(
            asignacion_canal_distribuidor.c.id_asignacion_canal_distribuidor == id_asignacion_canal_distribuidor
        )
        db.execute(query)
        return {"status": 200, "message": "Eliminacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}



