from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from database.db import meta, db


SalesBoss = Table("sc_sales_boss", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("employee", Integer, ForeignKey("sc_employee.id")),
    Column("city", Integer, ForeignKey("sc_city.id"))
)


meta.create_all(db)