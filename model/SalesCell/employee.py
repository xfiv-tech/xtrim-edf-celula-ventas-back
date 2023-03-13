from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from database.db import meta, db


Employee = Table("sc_employee", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable = False),
    Column("lastname", String(255), nullable = False),
    Column("id_number", String(13), unique = True, nullable = False),
    Column("address", String(255), nullable=True),
    Column("residence_city", String(255), nullable=True),
    Column("birth_date", DateTime),
    Column("email", String(255), nullable=True),
    Column("phone", String(10), nullable=False),
    Column("operator", Integer, ForeignKey("catalog_detail.id")),
    Column("phone_optional", String(10), nullable=False),
    Column("operator_optional", Integer, ForeignKey("catalog_detail.id")),
    Column("gender", Integer, ForeignKey("catalog_detail.id")),
    Column("status", Integer, ForeignKey("catalog_detail.id")),
    Column("created_at", DateTime),
)


meta.create_all(db)