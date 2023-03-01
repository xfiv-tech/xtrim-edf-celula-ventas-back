from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey
from database.db import meta, db

Channel = Table("channel", meta,
    Column("id_channel", Integer, primary_key=True, autoincrement=True),
    Column("channel", String(255), unique=True),
)

Mando = Table("mando", meta,
    Column("id_mando", Integer, primary_key=True, autoincrement=True),
    Column("mando", String(255), unique=True),
)

meta.create_all(db)