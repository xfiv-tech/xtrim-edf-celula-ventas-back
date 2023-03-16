from fastapi import Request, HTTPException
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

from function.function_jwt import read_token
load_dotenv()

Token = os.getenv("Xtrim_token")
DEV = os.getenv("DEV")


class ValidacionToken(APIRoute):
    try:
        def get_route_handler(self):
            original_route = super().get_route_handler()
            async def verify_token_middleware(request:Request):
                if DEV == "PRO": return await original_route(request)
                channel = request.headers['channel']
                if channel == "Web":
                    beare = request.headers['Authorization']
                    beare_token = read_token(beare.split(" ")[1])
                    if beare_token["status"] == 200:
                        return await original_route(request)
                    else:
                        return JSONResponse(content={"message": "Invalid Token"}, status_code=401)
                else:
                    token = request.headers['xtrim-api-key']
                    validado = validarToken(token)
                    if validado:
                        return await original_route(request)
                    else:
                        return JSONResponse(content={"message": "Invalid Token"}, status_code=401)
            return verify_token_middleware
    except Exception as e:
        raise HTTPException(status_code=405)


def validarToken(token):
    try:
        if token == str(Token):
            return token
        else:
            return False
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })