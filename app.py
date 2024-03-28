from fastapi import FastAPI, Request, HTTPException
from middleware.validacionToken import ValidacionToken
from routes.xtrim_provider import xtrim_provider


from fastapi.middleware.cors import CORSMiddleware
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

Token = os.getenv("Xtrim_token")
DEV = os.getenv("DEV")

app = FastAPI(
    title="XTRIM API",
    description="A simple API to manage contacts",
    version="1.0.0",
    # openapi_prefix="/back_edificios_dev",
    root_path="/back_edificios_dev" if DEV == "PRO" else "/",
    root_path_in_servers=True,
    authorizations={
        
    }
    
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(xtrim_provider)


# from fastapi import FastAPI

