
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from database.db import meta, db


LeaderSeller = Table("sc_leader_seller", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("leader_id", Integer, ForeignKey("sc_employee.id")),
    Column("seller_id", Integer, ForeignKey("sc_employee.id")),
    Column("created_at", DateTime),
)


meta.create_all(db)
