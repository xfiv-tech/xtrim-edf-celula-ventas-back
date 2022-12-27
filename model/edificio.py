from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, DateTime, ForeignKey, BLOB, Text
from database.db import meta, db

Edicifios = Table("edificio", meta, 
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("id_usuario", Integer),
    Column("idAdministrador", Integer, ForeignKey("administradores.id")),
    Column("coordenadas", String(255)),
    Column("id_edificio", Text(4294967295)),
    Column("sector", Text(4294967295)),
    Column("ciudad", Text(4294967295)),
    Column("ctaReferencia", String(255)), 
    Column("cedulaReferencia", String(255)), 
    Column("nombreEdificio", String(255)), 
    Column("referencia", String(255)), 
    Column("responsable", String(255)), 
    Column("adjunto", Text(4294967295)), 
    Column("data_creatd", DateTime), 
    Column("data_update", DateTime)
)

meta.create_all(db)