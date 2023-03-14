from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from database.db import meta, db


Catalog = Table("catalog", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("code", String(255), nullable = True)
)


CatalogDetail = Table("catalog_detail", meta, 
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("code", String(255),nullable=True),
    Column("level", Integer, nullable=True),
    Column("description", String(255), nullable=True),
    Column("catalog", Integer, ForeignKey("catalog.id")),
)


meta.create_all(db)