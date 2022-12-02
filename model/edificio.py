from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from database.db import meta, db

Edicifios = Table("edificio", meta, 
    Column("idAdministrador", Integer, ForeignKey("administradores.id")),
    Column("coordenadas", String(255)),
    Column("ctaReferencia", String(255)), 
    Column("nombreEdificio", String(255)), 
    Column("referencia", String(255)), 
    Column("adjunto", String(1000000000)), 
    Column("data_creatd", DateTime), 
    Column("data_update", DateTime)
)

meta.create_all(db)