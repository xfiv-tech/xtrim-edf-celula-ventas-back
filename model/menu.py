from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey
from database.db import meta, db

Menus = Table("menus", meta,
    Column("id_menus", Integer, primary_key=True, autoincrement=True),
    Column("id_roles", Integer, ForeignKey("roles.id_roles")),
    Column("menu", String(255)),
    Column("path", String(255)),
    Column("icon", String(255)),

)
meta.create_all(db)
