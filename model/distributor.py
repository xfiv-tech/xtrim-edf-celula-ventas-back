from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from database.db import meta, db


Distributor = Table("ecommerce_distributor_login", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user", String(255), nullable = False),
    Column("userId", String(255), nullable=True),
    Column("distributor", String(255), nullable=True),
    Column("token", String(500), nullable=True),
    Column("created_at", DateTime, nullable=False),
)


meta.create_all(db)