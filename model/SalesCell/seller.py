
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from database.db import meta, db


Seller = Table("sc_seller", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("seller", Integer, ForeignKey("sc_employee.id")),
    Column("equifax_user", String(20), nullable = True),
    Column("city", Integer, ForeignKey("sc_city.id")),
    Column("channel", Integer, ForeignKey("catalog_detail.id")),
    Column("modality", Integer, ForeignKey("catalog_detail.id")),
    Column("goal_volumen", Integer, nullable = False),
    Column("goal_dolars", Float, nullable = False),
    Column("os", Integer, ForeignKey("catalog_detail.id")),
    Column("status", Integer, ForeignKey("catalog_detail.id")),
    Column("date_in_sales_dept", DateTime, nullable = False),
    Column("date_out_sales_dept", DateTime, nullable = True),
    Column("inactive_days", Integer, default=0),
    Column("created_at", DateTime),
)


meta.create_all(db)
