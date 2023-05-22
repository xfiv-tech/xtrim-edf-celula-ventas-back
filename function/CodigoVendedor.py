import requests
import uuid
import json

from model.channel import RegistrarVendedor
from database.db import db

async def LoginCodigo():
    try:
        payload = json.dumps({
            "channel": "Celula_Ventas",
            "key": "YXBpbS1jbGllbnQ6N2M4ZmEyMDgtMmZjZC00YjhiLTk1ZjktYTIwZWJkODliYmRi",
            "realm": "realm-ecommerce",
            "type": "Basic"
        })
        login = requests.post("https://apix.grupotvcable.com/rest/token-api/v1.0/generate", data=payload, headers={'Content-Type': 'application/json'})
        print("Login",login.json())
        response = login.json()
        return response["data"]["token"]

    except Exception as e:
        print(e)


async def ConsultarVendedor(codigo):
    try:
        quey = db.execute(RegistrarVendedor.select().where(RegistrarVendedor.codigo == codigo)).fetchone()
        if quey == None:
            print("externalTransactionId",str(uuid.uuid1()))
            response = await LoginCodigo()
            payload = json.dumps({
                "channel": "TYTAN",
                "idVendor": codigo,
                "application": "Marketplace",
                "externalTransactionId": str(uuid.uuid1()),
            })
            code = requests.post("https://apix.grupotvcable.com/rest/salesperson-api/v1.0/queryvendor", data=payload, headers={'Authorization': 'Bearer ' + response, 'Content-Type': 'application/json'})
            print(code)
            vendedor = code.json()
            if(vendedor["code"] == 400):
                return False
            else:
                return vendedor["data"]
        else:
            return {
                "code": 400,
                "message": "El codigo ya existe"
            }
    except Exception as e:
        print(e)
