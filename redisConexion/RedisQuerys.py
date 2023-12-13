import json

from redisConexion.conexionRedis import dbRedis


async def SetterRedis(key, value):
    try:
        # el values hay que convertirlo a string para poderlo guardar en redis
        dbRedis.set(key, json.dumps(value))
        return True
    except Exception as e:
        print('Error al guardar en Redis', e)
        return False
    
    
async def GetterRedis(key):
    try:
        # el values hay que convertirlo a string para poderlo guardar en redis
        info = dbRedis.get(key)
        if info is None:
            return False
        else:
            return json.loads(info)
    except Exception as e:
        print('Error al obtener en Redis', e)
        return False
    
async def AddRedis(key, value):
    try:
        data = dbRedis.get(key)
        if data is None:
            return False
        data = json.loads(data)
        print("AddRedis", value)
        data.append(value)
        dbRedis.set(key, json.dumps(data))
        return True
    except Exception as e:
        print("Error al agregar redis", e)
        return False
    
# actualizar un iten del value de redis
async def UpdateRedis(key, value):
    try:
        if key == "vendedor":
            data = dbRedis.get(key)
            if data is None:
                return False
            data = json.loads(data)
            # actualizamos un item de todo el array de objetos
            print("UpdateRedis", value)
            for i in range(len(data)):
                if data[i]['id_registrar_vendedor'] == value['id_registrar_vendedor']:
                    data[i] = value
                    break
            dbRedis.set(key, json.dumps(data))
            print("UpdateRedis", data)
            return True
    except Exception as e:
        print("Error al actualizar redis", e)
        return False
    
# eliminar un iten del value de redis
async def DeleteRedis(key, value):
    try:
        if key == "vendedor":
            data = dbRedis.get(key)
            if data is None:
                return False
            data = json.loads(data)
            # eliminamos un item de todo el array de objetos
            for i in range(len(data)):
                if data[i]['id_registrar_vendedor'] == value:
                    data.pop(i)
                    break
            dbRedis.set(key, json.dumps(data))
            return True
    except Exception as e:
        print("Error al eliminar redis", e)
        return False
    