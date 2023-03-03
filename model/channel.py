from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey
from database.db import meta, db


Ciudad = Table("ciudad", meta,
    Column("id_ciudad", Integer, primary_key=True, autoincrement=True),
    Column("ciudad", String(255), unique=True),
    Column("region", String(255)),
)

Operador = Table("operador", meta,
    Column("id_operador", Integer, primary_key=True, autoincrement=True),
    Column("operador", String(255), unique=True),
)

SistemaOperativo = Table("sistema_operativo", meta,
    Column("id_sistema_operativo", Integer, primary_key=True, autoincrement=True),
    Column("sistema_operativo", String(255), unique=True),
)

Estados = Table("estados", meta,
    Column("id_estado", Integer, primary_key=True, autoincrement=True),
    Column("estado", String(255), unique=True),
)

Genero = Table("genero", meta,
    Column("id_genero", Integer, primary_key=True, autoincrement=True),
    Column("genero", String(255), unique=True),
)

Modalidad = Table("modalidad", meta,
    Column("id_modalidad", Integer, primary_key=True, autoincrement=True),
    Column("modalidad", String(255), unique=True),
)


Channel = Table("channel", meta,
    Column("id_channel", Integer, primary_key=True, autoincrement=True),
    Column("channel", String(255), unique=True),
)

Mando = Table("mando", meta,
    Column("id_mando", Integer, primary_key=True, autoincrement=True),
    Column("mando", String(255), unique=True),
)

# RegistroGerente = Table("registro_gerente", meta,
#     Column("id_gerente", Integer, primary_key=True, autoincrement=True),
#     Column("id_mando", Integer, ForeignKey("mando.id_mando")),
#     Column("id_channel", Integer, ForeignKey("channel.id_channel")),
#     Column("nombre", String(255)),
#     Column("apellido", String(255)),
#     Column("telefono", String(255)),
#     Column("email", String(255)),
#     Column("celula", String(255)),
#     Column("codigo", String(255)),
#     Column("fecha", DateTime),
#     Column("activo", Boolean),
# )

# RegistroJefeVentas = Table("registro_jefe_ventas", meta,
#     Column("id_jefe_ventas", Integer, primary_key=True, autoincrement=True),
#     Column("id_mando", Integer, ForeignKey("mando.id_mando")),
#     Column("id_channel", Integer, ForeignKey("channel.id_channel")),
#     Column("nombre", String(255)),
#     Column("apellido", String(255)),
#     Column("telefono", String(255)),
#     Column("email", String(255)),
#     Column("celula", String(255)),
#     Column("codigo", String(255)),
#     Column("fecha", DateTime),
#     Column("activo", Boolean),
# )

# RegistroLiderPeloton = Table("registro_lider_peloton", meta,
#     Column("id_lider_peloton", Integer, primary_key=True, autoincrement=True),
#     Column("id_mando", Integer, ForeignKey("mando.id_mando")),  
#     Column("id_channel", Integer, ForeignKey("channel.id_channel")),
#     Column("nombre", String(255)),
#     Column("apellido", String(255)),
#     Column("telefono", String(255)),
#     Column("email", String(255)),
#     Column("celula", String(255)),
#     Column("codigo", String(255)),
#     Column("fecha", DateTime),
#     Column("activo", Boolean),
# )

# RegistroVendedor = Table("registro_vendedor", meta,
#     Column("id_vendedor", Integer, primary_key=True, autoincrement=True),
#     Column("id_mando", Integer, ForeignKey("mando.id_mando")),
#     Column("id_channel", Integer, ForeignKey("channel.id_channel")),
#     Column("nombre", String(255)),
#     Column("apellido", String(255)),
#     Column("telefono", String(255)),
#     Column("email", String(255)),
#     Column("celula", String(255)),
#     Column("codigo", String(255)),
#     Column("fecha", DateTime),
#     Column("activo", Boolean),
# )


meta.create_all(db)