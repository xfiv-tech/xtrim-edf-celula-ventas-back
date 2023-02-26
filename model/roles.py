
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey

from database.db import meta, db

Roles = Table("roles", meta,
    Column("id_roles", Integer, primary_key=True, autoincrement=True),
    Column("rol", String(255)),
    Column("descripcion", String(255)),
    Column("data_created", DateTime),
    Column("data_update", DateTime)
)

meta.create_all(db)