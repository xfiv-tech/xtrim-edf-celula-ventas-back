from fastapi import Request, HTTPException
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
load_dotenv()

Token = os.getenv("Xtrim_token")


class ValidacionToken(APIRoute):
    try:
        def get_route_handler(self):
            original_route = super().get_route_handler()
            async def verify_token_middleware(request:Request):
                token = request.headers['xtrim-api-key']
                print(token)
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