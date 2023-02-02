from pydantic import BaseModel

class AdminCedula(BaseModel):
    cedula: str
    channel: str