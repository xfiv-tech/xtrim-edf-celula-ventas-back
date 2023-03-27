


from fastapi import HTTPException

from controller.AsignacionController import ListarCanalesAdminCiudad, ListarCanalesJVCiudad, ListarCiudadesAdminCiudad, ListarCiudadesJVCiudad


async def ExtraerCiuCanl(id: int, perfil: str):
    return {
        # "canal": EntityCanals(await ListarCanalesAdminCiudad(id)),
        "ciudad": EntityCiudads(await ListarCiudadesAdminCiudad(id))
    }
    

def EntityCanals(canal):
    canals = []
    for i in canal:
        canals.append({
            "id_channel": i["id_channel"],
            "channel": i["channel"]
        })
    return canals

def EntityCiudads(ciudad):
    ciudads = []
    for i in ciudad:
        ciudads.append({
            "id_ciudad": i["id_ciudad"],
            "ciudad": i["ciudad"]
        })
    return ciudads