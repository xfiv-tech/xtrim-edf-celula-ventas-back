import requests
import uuid
import json

from model.channel import RegistrarVendedor
from database.db import db
import urllib3
import urllib3
from urllib3.util.ssl_ import create_urllib3_context

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# python -c 'import ssl;
# print(ssl.OPENSSL_VERSION) = OpenSSL 3.0.3 3 May 2022


# corregir (MaxRetryError("HTTPSConnectionPool(host='apix.grupotvcable.com', port=443): Max retries exceeded with url: /rest/token-api/v1.0/generate (Caused by SSLError(SSLError(1, '[SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED] unsafe legacy renegotiation disabled (_ssl.c:1007)')))"),)


import time


async def LoginCodigo():
    for attempt in range(3):
        try:
            ctx = create_urllib3_context()
            ctx.load_default_certs()
            ctx.options |= 0x4
            with urllib3.PoolManager(ssl_context=ctx) as http:
                url = "https://apix.grupotvcable.com/rest/token-api/v1.0/generate"
                data = {
                    "channel": "Web",
                    "key": "YXBpbV9hdXRvc2VydmljaW86MTU4MzliNDYtZTJiNy00ZWNkLThmZWEtZDM1ZDlhNWJlNGI3",
                    "realm": "realm-ecommerce-autoservicio",
                    "type": "Basic",
                }
                encoded_data = json.dumps(data).encode("utf-8")
                r = http.request(
                    "POST",
                    url,
                    body=encoded_data,
                    headers={"Content-Type": "application/json"},
                    timeout=10.0,
                )

                if r.status == 200:
                    diccionario = json.loads(r.data.decode("utf-8"))
                    return diccionario["data"]["token"]
                else:
                    print(f"Error en la solicitud, estado HTTP: {r.status}")
                    return None

        except urllib3.exceptions.MaxRetryError as e:
            print(f"Reintento {attempt+1} fallido: {e}")
            time.sleep(2)

        except Exception as e:
            print(f"Error: {e}")
            return None

    print("Error: No se pudo obtener el token después de varios intentos.")
    return None


async def ConsultarVendedor(codigo):
    try:
        query = db.execute(
            RegistrarVendedor.select().where(
                RegistrarVendedor.c.codigo_vendedor == codigo
            )
        ).fetchone()
        db.commit()
        if query is None:
            print("externalTransactionId", str(uuid.uuid1()))
            response = await LoginCodigo()

            # Verificar si response es None
            if response is None:
                print("Error: No se pudo obtener el token")
                return {
                    "code": 500,
                    "message": "Error de autenticación, token no obtenido",
                }

            ctx = create_urllib3_context()
            ctx.load_default_certs()
            ctx.options |= 0x4  # ssl.OP_LEGACY_SERVER_CONNECT
            with urllib3.PoolManager(ssl_context=ctx) as http:
                url = "https://apix.grupotvcable.com/rest/salesperson-api/v1.0/queryvendor"
                data = {
                    "channel": "TYTAN",
                    "idVendor": codigo,
                    "application": "Marketplace",
                    "externalTransactionId": str(uuid.uuid1()),
                }
                encoded_data = json.dumps(data).encode("utf-8")
                headers = {
                    "Authorization": f"Bearer {response}",
                    "Content-Type": "application/json",
                }

                r = http.request("POST", url, body=encoded_data, headers=headers)

                if r.status == 200:
                    diccionario = json.loads(r.data.decode("utf-8"))
                    print(diccionario)
                    if diccionario.get("code") == 400:
                        return False
                    else:
                        return diccionario["data"]
                else:
                    print(f"Error en la solicitud: {r.status}")
                    return {"code": r.status, "message": "Error en la consulta"}

        else:
            return {"code": 400, "message": "El codigo ya existe"}
    except Exception as e:
        print("Error: ", e.args)
        return {"code": 500, "message": "Error en la ejecución"}
