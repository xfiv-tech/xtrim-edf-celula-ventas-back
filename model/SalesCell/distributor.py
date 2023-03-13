from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from database.db import meta, db


Distributor = Table("sc_distributor", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable = False),
    Column("city", Integer, ForeignKey("catalog_detail.id")),
    Column("responsible", String(255), nullable=True),
    Column("status", Integer, ForeignKey("catalog_detail.id")),
    Column("phone", String(255), nullable=True),
    Column("email", String(255), nullable=True),
    Column("date_in", DateTime, nullable=False),
    Column("date_out", DateTime, nullable=True),
)


meta.create_all(db)