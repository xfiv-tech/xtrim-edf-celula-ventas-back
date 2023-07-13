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

async def LoginCodigo():
    try:
        ctx = create_urllib3_context()
        ctx.load_default_certs()
        ctx.options |= 0x4  # ssl.OP_LEGACY_SERVER_CONNECT
        with urllib3.PoolManager(ssl_context=ctx) as http:
            url = "https://apix.grupotvcable.com/rest/token-api/v1.0/generate"
            data = {
                "channel": "Web",
                "key": "YXBpbV9hdXRvc2VydmljaW86MTU4MzliNDYtZTJiNy00ZWNkLThmZWEtZDM1ZDlhNWJlNGI3",
                "realm": "realm-ecommerce-autoservicio",
                "type": "Basic"
            }
            encoded_data = json.dumps(data).encode('utf-8')
            r = http.request("POST", url, body=encoded_data, headers={'Content-Type': 'application/json'})
            if r.status == 200:
                response = r.data.decode('utf-8')
                print("Login",r.data.decode('utf-8'))
                print("Login",type(response["data"]["token"]))
                return response["data"]["token"]
            else:
                return False

        # payload = json.dumps({
        #     "channel": "Web",
        #     "key": "YXBpbV9hdXRvc2VydmljaW86MTU4MzliNDYtZTJiNy00ZWNkLThmZWEtZDM1ZDlhNWJlNGI3",
        #     "realm": "realm-ecommerce-autoservicio",
        #     "type": "Basic"
        # })
        # login = requests.post("https://apix.grupotvcable.com/rest/token-api/v1.0/generate", data=payload, headers={'Content-Type': 'application/json'})
        # print("Login",login.json())
        # response = login.json()
        # return response["data"]["token"]

    except Exception as e:
        print("Error: 53",e.args)


async def ConsultarVendedor(codigo):
    try:
        quey = db.execute(RegistrarVendedor.select().where(RegistrarVendedor.c.codigo_vendedor == codigo)).fetchone()
        if quey == None:
            print("externalTransactionId",str(uuid.uuid1()))
            response = await LoginCodigo()
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
                encoded_data = json.dumps(data).encode('utf-8')
                r = http.request("POST", url, body=encoded_data, headers={'Authorization': 'Bearer ' + response, 'Content-Type': 'application/json'})
                if r.status == 200:
                    resp = r.data.decode('utf-8')
                    print(resp["data"])
                    if(resp["code"] == 400):
                        return False
                    else:
                        return resp["data"]


            # payload = json.dumps({
            #     "channel": "TYTAN",
            #     "idVendor": codigo,
            #     "application": "Marketplace",
            #     "externalTransactionId": str(uuid.uuid1()),
            # })
            # code = requests.post("https://apix.grupotvcable.com/rest/salesperson-api/v1.0/queryvendor", data=payload, headers={'Authorization': 'Bearer ' + response, 'Content-Type': 'application/json'})
            # print(code)
            # vendedor = code.json()
            # if(vendedor["code"] == 400):
            #     return False
            # else:
            #     return vendedor["data"]
        else:
            return {
                "code": 400,
                "message": "El codigo ya existe"
            }
    except Exception as e:
        print("Error: ",e.args)
