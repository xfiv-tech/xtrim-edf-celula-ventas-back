from fastapi import APIRouter, HTTPException
from controller.AsignacionController import AsignarCanalesAPCiudad, AsignarCanalesAdminCiudad, AsignarCanalesDistribuidor, AsignarCanalesGCiudad, AsignarCanalesGRciudad, AsignarCanalesJVCiudad, AsignarCiudadesAPCiudad, AsignarCiudadesAdminCiudad, AsignarCiudadesDistribuidor, AsignarCiudadesGCiudad, AsignarCiudadesGRegional, AsignarCiudadesJVCiudad, DeleteCanalesAPCiudad, DeleteCanalesAdminCiudad, DeleteCanalesDistribuidor, DeleteCanalesGCiudad, DeleteCanalesGRciudad, DeleteCanalesJVCiudad, DeleteCiudadesAPCiudad, DeleteCiudadesAdminCiudad, DeleteCiudadesDistribuidor, DeleteCiudadesGCiudad, DeleteCiudadesGRegional, DeleteCiudadesJVCiudad, ListarCanalesAPCiudad, ListarCanalesAdminCiudad, ListarCanalesDistribuidor, ListarCanalesGCiudad, ListarCanalesJVCiudad, ListarCiudadesAPCiudad, ListarCiudadesAdminCiudad, ListarCiudadesDistribuidor, ListarCiudadesGCiudad, ListarCiudadesGRegional, ListarCiudadesJVCiudad
from middleware.validacionToken import ValidacionToken
from model.ModelSchema.asignacionModel import ArrayAsigancionCanalA, ArrayAsigancionCanalAdmin, ArrayAsigancionCanalDistribuidor, ArrayAsigancionCanalGciudad, ArrayAsigancionCanalGregional, ArrayAsigancionCanalJefe, ArrayAsigancionCiudadA, ArrayAsigancionCiudadAdmin, ArrayAsigancionCiudadDistribuidor, ArrayAsigancionCiudadGciudad, ArrayAsigancionCiudadGreginal, ArrayAsigancionCiudadJefe

asignacion = APIRouter(route_class=ValidacionToken)

@asignacion.post("/asignacion_ciudades_gerente_regional", tags=["Asignacion de ciudades a gerente regional"])
async def asignacion_ciudades_gerente_regional(data: ArrayAsigancionCiudadGreginal):
    return await AsignarCiudadesGRegional(data)

@asignacion.get("/listar_ciudades_gerente_regional/{id_gerente_regional}", tags=["Listar ciudades de gerente regional"])
async def listar_ciudades_gerente_regional(id_gerente_regional: int):
    return await ListarCiudadesGRegional(id_gerente_regional)

@asignacion.delete("/eliminar_asignacion_ciudades_gerente_regional/{id_asignacion_ciudad_greginal}", tags=["Eliminar asignacion de ciudades a gerente regional"])
async def eliminar_asignacion_ciudades_gerente_regional(id_asignacion_ciudad_greginal: int):
    return await DeleteCiudadesGRegional(id_asignacion_ciudad_greginal)

@asignacion.post("/asignacion_canal_gerente_regional", tags=["Asignacion de canal a gerente regional"])
async def asignacion_canal_gerente_regional(data: ArrayAsigancionCanalGregional):
    return await AsignarCanalesGRciudad(data)

@asignacion.get("/listar_canal_gerente_regional/{id_gerente_regional}", tags=["Listar canales de gerente regional"])
async def listar_canal_gerente_regional(id_gerente_regional: int):
    return await ListarCiudadesGRegional(id_gerente_regional)

@asignacion.delete("/eliminar_asignacion_canal_gerente_regional/{id_asignacion_canal}", tags=["Eliminar asignacion de canal a gerente regional"])
async def eliminar_asignacion_canal_gerente_regional(id_asignacion_canal: int):
    return await DeleteCanalesGRciudad(id_asignacion_canal)

#GENTE CIUDAD
@asignacion.post("/asignacion_ciudades_gerente_ciudad", tags=["Asignacion de ciudades a gerente ciudad"])
async def asignacion_ciudades_gerente_ciudad(data: ArrayAsigancionCiudadGciudad):
    return await AsignarCiudadesGCiudad(data)

@asignacion.get("/listar_ciudades_gerente_ciudad/{id_gerente_ciudad}", tags=["Listar ciudades de gerente ciudad"])
async def listar_ciudades_gerente_ciudad(id_gerente_ciudad: int):
    return await ListarCiudadesGCiudad(id_gerente_ciudad)

@asignacion.delete("/eliminar_asignacion_ciudades_gerente_ciudad/{id_asignacion_ciudades_gerente_ciudad}", tags=["Eliminar asignacion de ciudades a gerente ciudad"])
async def eliminar_asignacion_ciudades_gerente_ciudad(id_asignacion_ciudades_gerente_ciudad: int):
    return await DeleteCiudadesGCiudad(id_asignacion_ciudades_gerente_ciudad)

@asignacion.get("/listar_canal_gerente_ciudad/{id_gerente_ciudad}", tags=["Listar canales de gerente ciudad"])
async def listar_canal_gerente_ciudad(id_gerente_ciudad: int):
    return await ListarCanalesGCiudad(id_gerente_ciudad)

@asignacion.delete("/eliminar_asignacion_canal_gerente_ciudad/{id_asignacion_canal_gerente_ciudad}", tags=["Eliminar asignacion de canal a gerente ciudad"])
async def eliminar_asignacion_canal_gerente_ciudad(id_asignacion_canal_gerente_ciudad: int):
    return await DeleteCanalesGCiudad(id_asignacion_canal_gerente_ciudad)

@asignacion.post("/asignacion_canal_gerente_ciudad", tags=["Asignacion de canal a gerente ciudad"])
async def asignacion_canal_gerente_ciudad(data: ArrayAsigancionCanalGciudad):
    return await AsignarCanalesGCiudad(data)

#Jefe de Ventas
@asignacion.get("/listar_canal_jefe_ventas/{id_jefe_venta}", tags=["Listar canales de jefe de ventas"])
async def listar_canal_jefe_ventas(id_jefe_venta: int):
    return await ListarCanalesJVCiudad(id_jefe_venta)

@asignacion.post("/asignacion_canal_jefe_ventas", tags=["Asignacion de canal a jefe de ventas"])
async def asignacion_canal_jefe_ventas(data: ArrayAsigancionCanalJefe):
    return await AsignarCanalesJVCiudad(data)

@asignacion.delete("/eliminar_asignacion_canal_jefe_ventas/{id_asignacion_canal_jefe_ventas}", tags=["Eliminar asignacion de canal a jefe de ventas"])
async def eliminar_asignacion_canal_jefe_ventas(id_asignacion_canal_jefe_ventas: int):
    return await DeleteCanalesJVCiudad(id_asignacion_canal_jefe_ventas)

@asignacion.get("/listar_ciudades_jefe_ventas/{id_jefe_venta}", tags=["Listar ciudades de jefe de ventas"])
async def listar_ciudades_jefe_ventas(id_jefe_venta: int):
    return await ListarCiudadesJVCiudad(id_jefe_venta)

@asignacion.delete("/eliminar_asignacion_ciudades_jefe_ventas/{id_asignacion_ciudades_jefe_ventas}", tags=["Eliminar asignacion de ciudades a jefe de ventas"])
async def eliminar_asignacion_ciudades_jefe_ventas(id_asignacion_ciudades_jefe_ventas: int):
    return await DeleteCiudadesJVCiudad(id_asignacion_ciudades_jefe_ventas)

@asignacion.post("/asignacion_ciudades_jefe_ventas", tags=["Asignacion de ciudades a jefe de ventas"])
async def asignacion_ciudades_jefe_ventas(data: ArrayAsigancionCiudadJefe):
    return await AsignarCiudadesJVCiudad(data)

#Administrador de proyecto
@asignacion.get("/listar_canal_administrador_proyecto/{id_admin_proyecto}", tags=["Listar canales de administrador de proyecto"])
async def listar_canal_administrador(id_admin_proyecto: int):
    return await ListarCanalesAPCiudad(id_admin_proyecto)

@asignacion.post("/asignacion_canal_administrador_proyecto", tags=["Asignacion de canal a administrador de proyecto"])
async def asignacion_canal_administrador(data: ArrayAsigancionCanalAdmin):
    return await AsignarCanalesAPCiudad(data)

@asignacion.delete("/eliminar_asignacion_canal_administrador_v/{id_asignacion_ciudades_admin_proyectos}", tags=["Eliminar asignacion de canal a administrador de proyecto"])
async def eliminar_asignacion_canal_administrador(id_asignacion_ciudades_admin_proyectos: int):
    return await DeleteCanalesAPCiudad(id_asignacion_ciudades_admin_proyectos)

@asignacion.get("/listar_ciudades_administrador_proyecto/{id_admin_proyecto}", tags=["Listar ciudades de administrador de proyecto"])
async def listar_ciudades_administrador(id_admin_proyecto: int):
    return await ListarCiudadesAPCiudad(id_admin_proyecto)

@asignacion.delete("/eliminar_asignacion_ciudades_administrador_proyecto/{id_asignacion_ciudades_administrador}", tags=["Eliminar asignacion de ciudades a administrador de proyecto"])
async def eliminar_asignacion_ciudades_administrador(id_asignacion_ciudades_administrador: int):
    return await DeleteCiudadesAPCiudad(id_asignacion_ciudades_administrador)

@asignacion.post("/asignacion_ciudades_administrador_proyecto", tags=["Asignacion de ciudades a administrador de proyecto"])
async def asignacion_ciudades_administrador(data: ArrayAsigancionCiudadAdmin):
    return await AsignarCiudadesAPCiudad(data)

#Distribuidor
@asignacion.get("/listar_canal_distribuidor/{id_distribuidor}", tags=["Listar canales de distribuidor"])
async def listar_canal_distribuidor(id_distribuidor: int):
    return await ListarCanalesDistribuidor(id_distribuidor)

@asignacion.post("/asignacion_canal_distribuidor", tags=["Asignacion de canal a distribuidor"])
async def asignacion_canal_distribuidor(data: ArrayAsigancionCanalDistribuidor):
    return await AsignarCanalesDistribuidor(data)

@asignacion.delete("/eliminar_asignacion_canal_distribuidor/{id_asignacion_canal_distribuidor}", tags=["Eliminar asignacion de canal a distribuidor"])
async def eliminar_asignacion_canal_distribuidor(id_asignacion_canal_distribuidor: int):
    return await DeleteCanalesDistribuidor(id_asignacion_canal_distribuidor)

@asignacion.get("/listar_ciudades_distribuidor/{id_distribuidor}", tags=["Listar ciudades de distribuidor"])
async def listar_ciudades_distribuidor(id_distribuidor: int):
    return await ListarCiudadesDistribuidor(id_distribuidor)

@asignacion.delete("/eliminar_asignacion_ciudades_distribuidor/{id_asignacion_ciudades_distribuidor}", tags=["Eliminar asignacion de ciudades a distribuidor"])
async def eliminar_asignacion_ciudades_distribuidor(id_asignacion_ciudades_distribuidor: int):
    return await DeleteCiudadesDistribuidor(id_asignacion_ciudades_distribuidor)

@asignacion.post("/asignacion_ciudades_distribuidor", tags=["Asignacion de ciudades a distribuidor"])
async def asignacion_ciudades_distribuidor(data: ArrayAsigancionCiudadDistribuidor):
    return await AsignarCiudadesDistribuidor(data)


#Administrador 
@asignacion.get("/listar_canal_administrador/{id_administrador}", tags=["Listar canales de administrador"])
async def listar_canal_administrador(id_administrador: int):
    return await ListarCanalesAdminCiudad(id_administrador)

@asignacion.post("/asignacion_canal_administrador", tags=["Asignacion de canal a administrador"])
async def asignacion_canal_administrador(data: ArrayAsigancionCanalA):
    return await AsignarCanalesAdminCiudad(data)

@asignacion.delete("/eliminar_asignacion_canal_administrador/{id_asignacion_canal_admin}", tags=["Eliminar asignacion de canal a administrador"])
async def eliminar_asignacion_canal_administrador(id_asignacion_canal_admin: int):
    return await DeleteCanalesAdminCiudad(id_asignacion_canal_admin)

@asignacion.get("/listar_ciudades_administrador/{id_administrador}", tags=["Listar ciudades de administrador de proyecto"])
async def listar_ciudades_administrador(id_administrador: int):
    return await ListarCiudadesAdminCiudad(id_administrador)

@asignacion.delete("/eliminar_asignacion_ciudades_administrador/{id_asignacion_ciudades_admin}", tags=["Eliminar asignacion de ciudades a administrador"])
async def eliminar_asignacion_ciudades_administrador(id_asignacion_ciudades_admin: int):
    return await DeleteCiudadesAdminCiudad(id_asignacion_ciudades_admin)

@asignacion.post("/asignacion_ciudades_administrador", tags=["Asignacion de ciudades a administrador"])
async def asignacion_ciudades_administrador(data: ArrayAsigancionCiudadA):
    return await AsignarCiudadesAdminCiudad(data)