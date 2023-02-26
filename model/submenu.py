from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey
from database.db import meta, db

Submenus = Table("submenus", meta,
    Column("id_menus", Integer, ForeignKey("menus.id_menus")),
    Column("submenu", String(255)),
    Column("path", String(255)),
    Column("icon", String(255)),
)
meta.create_all(db)
