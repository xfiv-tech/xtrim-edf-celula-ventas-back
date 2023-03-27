from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from os import getenv
from fastapi.responses import JSONResponse
import json
from dotenv import load_dotenv
import os
load_dotenv()
import jwt
SECRET = getenv("SECRET")


def expire_date(days: int):
    date = datetime.now()
    new_date = date + timedelta(days=days)
    return new_date


def write_token(data: dict):
    try:
        encoded = jwt.encode({**data, "exp": expire_date(1)}, SECRET, algorithm="HS256")
        return encoded
    except Exception as e:
        print("write_token",e)
        return JSONResponse(status_code=401, content={"message": "Invalid Token"})

def read_token(token: str):
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        print("read_token",data)
        return {
            "data": data,
            "status": 200
        }
    except exceptions.ExpiredSignatureError:
        return {
            "message": "Token Expired",
            "status": 401
        }
    except exceptions.DecodeError:
        return {
            "message": "Invalid Token",
            "status": 401
        }

def decode_token(token: str):
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        return data
    except exceptions.ExpiredSignatureError:
        return {
            "message": "Token Expired",
            "status": 401
        }
    except exceptions.DecodeError:
        return {
            "message": "Invalid Token",
            "status": 401
        }