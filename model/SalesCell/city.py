from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from database.db import meta, db


City = Table("sc_city", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("city", Integer, ForeignKey("catalog_detail.id")),
    Column("type", Integer, ForeignKey("catalog_detail.id")),
    Column("region", Integer, ForeignKey("catalog_detail.id")),
    Column("status", Integer, ForeignKey("catalog_detail.id")),
    Column("manager_region", Integer, ForeignKey("sc_manager.id")),
    Column("manager_city", Integer, ForeignKey("sc_manager.id")),
    Column("created_at", DateTime),
)


meta.create_all(db)