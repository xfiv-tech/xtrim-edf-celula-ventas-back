from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from database.db import meta, db


Administrator = Table("sc_administrator", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("city", Integer, ForeignKey("sc_city.id")),
    Column("user", Integer, ForeignKey("sc_employee.id")),
    Column("status", Integer, ForeignKey("catalog_detail.id")),
    Column("created_at", DateTime),
)


meta.create_all(db)