from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from database.db import meta, db


Administrator = Table("sc_administrator", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("city", Integer, ForeignKey("City.id")),
    Column("user", Integer, ForeignKey("Employee.id")),
    Column("status", Integer, ForeignKey("CatalogDetail.id")),
)


meta.create_all(db)