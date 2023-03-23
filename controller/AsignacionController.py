


from model.ModelSchema.asignacionModel import ArrayAsigancionCanalAdmin, ArrayAsigancionCanalDistribuidor
from model.ModelSchema.asignacionModel import ArrayAsigancionCanalGciudad, ArrayAsigancionCanalGregional
from model.ModelSchema.asignacionModel import ArrayAsigancionCanalJefe, ArrayAsigancionCiudadAdmin
from model.ModelSchema.asignacionModel import ArrayAsigancionCiudadDistribuidor, ArrayAsigancionCiudadGciudad
from model.ModelSchema.asignacionModel import ArrayAsigancionCiudadGreginal, ArrayAsigancionCiudadJefe
from model.channel import Channel, Ciudad, asignacion_ciudades_gerente_regional, asiganacion_canal_gerente_regional
from model.channel import asignacion_ciudades_gerente_ciudad,asignacion_canal_gerente_ciudad
from model.channel import asignacion_ciudades_jefe_ventas,asignacion_canal_jefe_ventas
from model.channel import asignacion_ciudades_admin_proyectos,asignacion_canal_admin_proyectos
from model.channel import asignacion_ciudades_distribuidor,asignacion_canal_distribuidor
from model.channel import asignacion_ciudades_admin,asignacion_canal_admin


from database.db import db
#Gerente regional
async def AsignarCiudadesGRegional(data: ArrayAsigancionCiudadGreginal):
    try:
        for i in data.data:
            print(i)
            if i.id_gerente_regional != 0 and i.id_ciudad != 0:
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
        print(id_gerente_regional)
        query = asignacion_ciudades_gerente_regional.select().where(
            asignacion_ciudades_gerente_regional.c.id_gerente_regional == id_gerente_regional
        )
        asignacion = db.execute(query).fetchall()
        infoData = []
        for i in asignacion:
            query = Ciudad.select().where(Ciudad.c.id_ciudad == i.id_ciudad)
            ciu = db.execute(query).fetchone()
            infoData.append({
                "id_asignacion_ciudades": i.id_asignacion_ciudades,
                "id_ciudad": i.id_ciudad,
                "id_gerente_regional": i.id_gerente_regional,
                "ciudad": ciu.ciudad
            })
        return infoData
    except Exception as e:
        print(e.args)
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
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            infoData.append({
                "id_asignacion_canal": i.id_asignacion_canal,
                "id_channel": i.id_channel,
                "id_gerente_regional": i.id_gerente_regional,
                "channel": i.channel
            })
        return infoData
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
        query = asignacion_ciudades_gerente_ciudad.join(Ciudad, asignacion_ciudades_gerente_ciudad.c.id_ciudad == Ciudad.c.id_ciudad).select().where(
            asignacion_ciudades_gerente_ciudad.c.id_gerente_ciudad == id_gerente_ciudad
        )
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            infoData.append({
                "id_asignacion_ciudades_gerente_ciudad": i.id_asignacion_ciudades_gerente_ciudad,
                "id_ciudad": i.id_ciudad,
                "id_gerente_ciudad": i.id_gerente_ciudad,
                "region": i.region,
                "ciudad": i.ciudad
            })
        return infoData
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
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            infoData.append({
                "id_asignacion_canal_gerente_ciudad": i.id_asignacion_canal_gerente_ciudad,
                "id_channel": i.id_channel,
                "id_gerente_ciudad": i.id_gerente_ciudad,
                "channel": i.channel
            })
        return infoData
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
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            infoData.append({
                "id_asignacion_ciudades_jefe_ventas": i.id_asignacion_ciudades_jefe_ventas,
                "id_ciudad": i.id_ciudad,
                "id_jefe_venta": i.id_jefe_venta,
                "ciudad": i.ciudad
            })
            return infoData
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
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            infoData.append({
                "id_asignacion_canal_jefe_ventas": i.id_asignacion_canal_jefe_ventas,
                "id_channel": i.id_channel,
                "id_jefe_venta": i.id_jefe_venta,
                "channel": i.channel
            })
        return infoData
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
async def AsignarCiudadesAPCiudad(data):
    try:
        for i in data.data:
            if i.id_admin_proyectos != 0 and i.id_ciudad != 0:
                query = asignacion_ciudades_admin_proyectos.insert().values(
                    id_ciudad=i.id_ciudad,
                    id_admin_proyectos=i.id_admin_proyectos,
                )
                db.execute(query)
        return {"status": 200, "message": "Asignacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}

async def ListarCiudadesAPCiudad(id_admin_proyectos: int):
    try:
        query = asignacion_ciudades_admin_proyectos.join(Ciudad, asignacion_ciudades_admin_proyectos.c.id_ciudad == Ciudad.c.id_ciudad).select().where(
            asignacion_ciudades_admin_proyectos.c.id_admin_proyectos == id_admin_proyectos
        )
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            infoData.append({
                "id_asignacion_ciudades_admin_proyectos": i.id_asignacion_ciudades_admin_proyectos,
                "id_ciudad": i.id_ciudad,
                "id_admin_proyectos": i.id_admin_proyectos,
                "ciudad": i.ciudad
            })
        return infoData
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def DeleteCiudadesAPCiudad(id_admin_proyectos: int):
    try:
        query = asignacion_ciudades_admin_proyectos.delete().where(
            asignacion_ciudades_admin_proyectos.c.id_admin_proyectos == id_admin_proyectos
        )
        db.execute(query)
        return {"status": 200, "message": "Eliminacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def AsignarCanalesAPCiudad(data: ArrayAsigancionCanalAdmin):
    try:
        for i in data.data:
            if i.id_channel != 0 and i.id_admin_proyectos != 0:
                query = asignacion_canal_admin_proyectos.insert().values(
                    id_channel=i.id_channel,
                    id_admin_proyectos=i.id_admin_proyectos,
                )
                db.execute(query)
        return {"status": 200, "message": "Asignacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def ListarCanalesAPCiudad(id_admin_proyectos: int):
    try:
        query = asignacion_canal_admin_proyectos.join(Channel, asignacion_canal_admin_proyectos.c.id_channel == Channel.c.id_channel).select().where(
            asignacion_canal_admin_proyectos.c.id_admin_proyectos == id_admin_proyectos
        )
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            infoData.append({
                "id_asignacion_canal_admin_proyectos": i.id_asignacion_canal_admin_proyectos,
                "id_channel": i.id_channel,
                "id_admin_proyectos": i.id_admin_proyectos,
                "channel": i.channel
            })
        return infoData
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def DeleteCanalesAPCiudad(id_admin_proyectos: int):
    try:
        query = asignacion_canal_admin_proyectos.delete().where(
            asignacion_canal_admin_proyectos.c.id_admin_proyectos == id_admin_proyectos
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
    
async def ListarCiudadesDistribuidor(id_registrar_distribuidor: int):
    try:
        query = asignacion_ciudades_distribuidor.join(Ciudad, asignacion_ciudades_distribuidor.c.id_ciudad == Ciudad.c.id_ciudad).select().where(
            asignacion_ciudades_distribuidor.c.id_registrar_distribuidor == id_registrar_distribuidor
        )
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            infoData.append({
                "id_asignacion_ciudades_distribuidor": i.id_asignacion_ciudades_distribuidor,
                "id_ciudad": i.id_ciudad,
                "id_distribuidor": i.id_registrar_distribuidor,
                "ciudad": i.ciudad
            })
        return infoData
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
    
async def ListarCanalesDistribuidor(id_registrar_distribuidor: int):
    try:
        query = asignacion_canal_distribuidor.join(Channel, asignacion_canal_distribuidor.c.id_channel == Channel.c.id_channel).select().where(
            asignacion_canal_distribuidor.c.id_registrar_distribuidor == id_registrar_distribuidor
        )
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            infoData.append({
                "id_asignacion_canal_distribuidor": i.id_asignacion_canal_distribuidor,
                "id_channel": i.id_channel,
                "id_distribuidor": i.id_registrar_distribuidor,
                "channel": i.channel
            })
        return infoData
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



#Asignacion de Administradores
async def AsignarCiudadesAdminCiudad(data):
    try:
        for i in data.data:
            if i.id_administrador != 0 and i.id_ciudad != 0:
                query = asignacion_ciudades_admin.insert().values(
                    id_ciudad=i.id_ciudad,
                    id_administrador=i.id_administrador,
                )
                db.execute(query)
        return {"status": 200, "message": "Asignacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}

async def ListarCiudadesAdminCiudad(id_administrador: int):
    try:
        query = asignacion_ciudades_admin.join(Ciudad, asignacion_ciudades_admin.c.id_ciudad == Ciudad.c.id_ciudad).select().where(
            asignacion_ciudades_admin.c.id_administrador == id_administrador
        )
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            infoData.append({
                "id_asignacion_ciudades_admin": i.id_asignacion_ciudades_admin,
                "id_ciudad": i.id_ciudad,
                "id_administrador": i.id_administrador,
                "ciudad": i.ciudad
            })
        return infoData
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def DeleteCiudadesAdminCiudad(id_administrador: int):
    try:
        query = asignacion_ciudades_admin.delete().where(
            asignacion_ciudades_admin.c.id_administrador == id_administrador
        )
        db.execute(query)
        return {"status": 200, "message": "Eliminacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def AsignarCanalesAdminCiudad(data):
    try:
        for i in data.data:
            if i.id_channel != 0 and i.id_administrador != 0:
                query = asignacion_canal_admin.insert().values(
                    id_channel=i.id_channel,
                    id_administrador=i.id_administrador,
                )
                db.execute(query)
        return {"status": 200, "message": "Asignacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def ListarCanalesAdminCiudad(id_administrador: int):
    try:
        query = asignacion_canal_admin.join(Channel, asignacion_canal_admin.c.id_channel == Channel.c.id_channel).select().where(
            asignacion_canal_admin.c.id_administrador == id_administrador
        )
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            infoData.append({
                "id_asignacion_canal_admin": i.id_asignacion_canal_admin,
                "id_channel": i.id_channel,
                "id_administrador": i.id_administrador,
                "channel": i.channel
            })
        return infoData
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
async def DeleteCanalesAdminCiudad(id_administrador: int):
    try:
        query = asignacion_canal_admin.delete().where(
            asignacion_canal_admin.c.id_administrador == id_administrador
        )
        db.execute(query)
        return {"status": 200, "message": "Eliminacion exitosa"}
    except Exception as e:
        return {"status": 400, "message": str(e)}
 
