from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from database.db import meta, db

Usuarios = Table("usuarios", meta, 
    Column("id", Integer, primary_key=True), 
    Column("nombreCompleto", String(255)), 
    Column("email", String(255), unique=True), 
    Column("usuario", String(255)), 
    Column("password", String(1000)), 
    Column("data_creatd", DateTime), 
    Column("data_update", DateTime)
)

meta.create_all(db)
