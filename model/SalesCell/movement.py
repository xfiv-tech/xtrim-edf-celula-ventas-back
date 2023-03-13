from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from database.db import meta, db


Movement = Table("sc_movement", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("category", Integer, ForeignKey("CatalogDetail.id")),
    Column("employee", Integer, ForeignKey("Employee.id")),
    Column("previous", Integer, ForeignKey("CatalogDetail.id")),
    Column("current", Integer, ForeignKey("CatalogDetail.id")),
    Column("created_at", DateTime),
)


meta.create_all(db)