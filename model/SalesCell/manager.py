
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from database.db import meta, db


Manager = Table("sc_manager", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("manager", Integer, ForeignKey("sc_employee.id")),
    Column("type", Integer, ForeignKey("catalog_detail.id")),
    Column("created_at", DateTime),
)


meta.create_all(db)
