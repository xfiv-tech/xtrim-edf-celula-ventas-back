import requests
import uuid
# session = requests.Session()
# session.verify = False

async def LoginCodigo():
    try:

        login = requests.post("https://apix.grupotvcable.com/rest/token-api/v1.0/generate", data={
            "channel": "Celula_Ventas",
            "key": "YXBpbS1jbGllbnQ6N2M4ZmEyMDgtMmZjZC00YjhiLTk1ZjktYTIwZWJkODliYmRi",
            "realm": "realm-ecommerce",
            "type": "Basic"
        })
        print("Login",login.json())
        response = login.json()
        return response["data"]["token"]

    except Exception as e:
        print(e)


async def ConsultarVendedor(codigo):
    try:
        print("externalTransactionId",str(uuid.uuid1()))
        response = await LoginCodigo()
        code = requests.post("https://apix.grupotvcable.com/rest/salesperson-api/v1.0/queryvendor", data={
            "channel": "TYTAN",
            "idVendor": codigo,
            "application": "Marketplace",
            "externalTransactionId": str(uuid.uuid1()),
        }, headers={
            'Authorization': 'Bearer ' + response,
        })
        print(code)
        vendedor = code.json()
        if(vendedor["code"] == 400):
            return False
        else:
            return vendedor["data"]
    except Exception as e:
        print(e)
