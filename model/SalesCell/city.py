from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from database.db import meta, db


City = Table("sc_city", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable = False),
    Column("type", Integer, ForeignKey("CatalogDetail.id")),
    Column("region", Integer, ForeignKey("CatalogDetail.id")),
    Column("status", Integer, ForeignKey("CatalogDetail.id")),
    Column("manager_region", Integer, ForeignKey("Employee.id")),
    Column("manager_city", Integer, ForeignKey("Employee.id")),

)


meta.create_all(db)