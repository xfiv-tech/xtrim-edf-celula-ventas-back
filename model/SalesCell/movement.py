from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from database.db import meta, db


Movement = Table("sc_movement", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("category", Integer, ForeignKey("catalog_detail.id")),
    Column("employee", Integer, ForeignKey("sc_mployee.id")),
    Column("previous", Integer, ForeignKey("catalog_detail.id")),
    Column("current", Integer, ForeignKey("catalog_detail.id")),
    Column("created_at", DateTime),
)


meta.create_all(db)