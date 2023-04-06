


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
    