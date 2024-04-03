import requests

from database.db import db
from model.ModelSchema.distributorModel import DistributorModel
from model.distributor import Distributor
from sqlalchemy import func, and_

from fastapi import APIRouter, Response, Depends, HTTPException, status, File
from fastapi.responses import RedirectResponse
from schemas.loginDistributor import LoginToken, DistributorLogin, DistributorLoginResponse, DistributorLoginDecrypt
from datetime import datetime
from middleware.validacionToken import ValidacionToken
from function.encryptMethods import encrypt_object, decrypt_object
from starlette.status import HTTP_204_NO_CONTENT
import qrcode
from io import BytesIO
import json

from dotenv import load_dotenv
import os

load_dotenv()


xtrim_provider = APIRouter()
@xtrim_provider.post("/create_qr_to_login", tags=["Distributors"])
def create_qr_to_login(distributorLogin:DistributorLogin):
    try:
        memory = BytesIO()
        base_url = os.getenv("URL_TO_EXPOSE_QR")

        user = json.dumps({
            "dni": distributorLogin.dni,
            "password": distributorLogin.password,
            "distributor": distributorLogin.distributor
        })

        encrypt = encrypt_object(user)
        url_qr = f"{base_url}/?encode={encrypt}"
        print(url_qr)

        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5,
        )
        qr.add_data(url_qr)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        img.save(memory)
        memory.seek(0)

        return Response(content=memory.getvalue(), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "data": str(e)
        })



@xtrim_provider.get("/expose/", tags=["Distributors"],response_class=RedirectResponse)
def decrypt_url_and_login(encode: str)-> RedirectResponse:
    try:
        decrypt = decrypt_object(encode)

        try:
            json_data = json.loads(decrypt)
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
            json_data = {}

        user_dict = DistributorLogin(**json_data)
        token = get_login_token()

        user_login = login_access_xtrim_provider(user_dict, token)
        user_access = user_login["user"]
        user = user_access["displayName"]

        response_data = {
        "token": token,
        "user": user
        }
        encoded_response = json.dumps(response_data)

        url_to_redirect = f"http://localhost:4200/compra-en-linea/login?_Response={encoded_response}"
        return RedirectResponse(url=url_to_redirect)
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "data": str(e)
        })


def add_distributor_login(distributorLogin: DistributorModel):
    try:
        result = db.execute(Distributor.insert()
            .values(user = distributorLogin.user,
                    userId = (distributorLogin.userId),
                    distributor = (distributorLogin.distributor),
                    token = (distributorLogin.token),
                    created_at = (datetime.now())))
        return "success"
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


def search_valid_token(dist: str):
    current_datetime = func.now()
    try:
        print(f"Searching token for: {dist}")
        query = Distributor.select().where(and_(Distributor.c.distributor == dist, Distributor.c.created_at <= current_datetime))
        first_result = db.execute(query).first()

        if first_result:
            id_, user, userId, distributor, token, created_at = first_result
            json_data = {
                "id": id_,
                "user": user,
                "userId": userId,
                "distributor": distributor,
                "token": token,
                "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S")  # Convertir el objeto datetime a una cadena en el formato deseado
            }

            result = json.dumps(json_data)
            return result
        else:
            print("No se encontraron resultados.")
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
    
    
def get_login_token():
    try:
        url = os.getenv("URL_LOGIN_TOKEN")
        
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'tenant': os.getenv("TENANT_ENGINE_V2")
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200: 
            data_dict = response.json()
            login_token = LoginToken(**data_dict)
            return login_token.token
        else:
            return json.dumps({'error': 'Error'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


def login_access_xtrim_provider(distributorLogin:DistributorLogin, login_token):
    try:
        tenant = os.getenv("TENANT_ENGINE_V2")
        url = os.getenv("URL_LOGIN_ACCESS_XTRIM_PROVIDER")

        payload = json.dumps({
            "dni": distributorLogin.dni,
            "password": distributorLogin.password
        })

        headers = {
            'Content-Type': 'application/json',
            'tenant': tenant,
            'Authorization': f"Bearer {login_token}"
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200: 
            data_dict = response.json()
            return data_dict
        else:
            return json.dumps({'error': 'Error'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")