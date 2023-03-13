
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from database.db import meta, db


Seller = Table("sc_seller", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("seller_id", Integer, ForeignKey("Employee.id")),
    Column("equifax_user", String(20), nullable = True),
    Column("city", Integer, ForeignKey("City.id")),
    Column("channel", Integer, ForeignKey("CatalogDetail.id")),
    Column("is_leader", Boolean, default = False),
    Column("modality", Integer, ForeignKey("CatalogDetail.id")),
    Column("goal_volumen", Integer, nullable = False),
    Column("goal_dolars", Float, nullable = False),
    Column("os", Integer, ForeignKey("CatalogDetail.id")),
    Column("status", Integer, ForeignKey("CatalogDetail.id")),
    Column("date_in_sales_dept", DateTime, nullable = False),
    Column("date_out_sales_dept", DateTime, nullable = False),
    Column("inactive_days", Integer, default=0),
)


meta.create_all(db)
