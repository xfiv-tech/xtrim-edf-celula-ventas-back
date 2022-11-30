from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from database.db import meta, db

Administradores = Table("administradores", meta, 
    Column("id", Integer, primary_key=True), 
    Column("nombreAdministrador", String(255)), 
    Column("cedula", String(255), unique=True), 
    Column("email", String(255), unique=True), 
    Column("telefono", String(12)), 
    Column("telefono_opt", String(12)), 
    Column("data_creatd", DateTime), 
    Column("data_update", DateTime)
)

meta.create_all(db)