import requests
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
async def create_qr_to_login(distributorLogin:DistributorLogin):
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



@xtrim_provider.get("/redirect/", tags=["Distributors"])
async def decrypt_url_and_login(encode: str):
    try:
        decrypt = decrypt_object(encode)

        try:
            json_data = json.loads(decrypt)
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
            json_data = {}

        user_dict = DistributorLogin(**json_data)
        login_token = get_login_token()
        print(f"login_token: {login_token}")
        user_login = login_access_xtrim_provider(user_dict, login_token)

        user_access = user_login["user"]
        user_data_access = json.dumps(user_access)
        print(f"user login: {user_data_access}")

        responseSite = RedirectResponse(url="https://ecommerce-web.intelnexo.com/vendor/compra-en-linea/cobertura/16")
        responseSite.set_cookie(
            key="user",
            value=user_data_access, 
            max_age=3600,
            httponly=True,
        )
        responseSite.set_cookie(
            key="token",
            value=f"Bearer {login_token}",
            max_age=3600 * 12,
            httponly=True,
        )

        return responseSite

    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "data": str(e)
        })

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