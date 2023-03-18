from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
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

RegistrarVendedor = Table("registrar_vendedor", meta,
    Column("id_registrar_vendedor", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, ForeignKey("channel.id_channel")),
    Column("id_ciudad", Integer, ForeignKey("ciudad.id_ciudad")),
    Column("id_operador", Integer, ForeignKey("operador.id_operador")),
    Column("id_sistema_operativo", Integer, ForeignKey("sistema_operativo.id_sistema_operativo")),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("id_genero", Integer, ForeignKey("genero.id_genero")),
    Column("id_modalidad", Integer, ForeignKey("modalidad.id_modalidad")),
    Column("cedula", String(255)),
    Column("codigo_vendedor", String(255), unique=True),
    Column("usuario_equifax", String(255)),
    Column("nombre_vendedor", String(255)),
    Column("fecha_ingreso", String(255)),
    Column("id_gerente", Integer, nullable=True, default=0),
    Column("id_gerente_regional", Integer, nullable=True, default=0),
    Column("id_gerente_ciudad", Integer, nullable=True, default=0),
    Column("id_jefe_venta", Integer, nullable=True),
    Column("id_lider_peloton", Integer, nullable=True, default=0),
    Column("ciudad_gestion", String(255)),
    Column("lider_check", Boolean, default=False),
    Column("meta_volumen", Integer, default=0),
    Column("meta_dolares", Float, default=0.0),
    Column("fecha_salida", String(255), nullable=True),
    Column("sector_residencia", String(255)),
    Column("email", String(255)),
    Column("cedula", String(255)),
    Column("dias_inactivo", Integer, default=0),
)

RegistrarDistribuidor = Table("registrar_distribuidor", meta,
    Column("id_registrar_distribuidor", Integer, primary_key=True, autoincrement=True),
    Column("id_ciudad", Integer, ForeignKey("channel.id_channel")),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("nombre_distribuidor", String(255)),
    Column("responsable", String(255)),
    Column("telefono", String(255)),
    Column("email", String(255)),
    Column("fecha_ingreso", String(255)),
    Column("fecha_salida", String(255), nullable=True)
)

RegistrarGerente = Table("registrar_gerente", meta,
    Column("id_gerente", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, ForeignKey("channel.id_channel")),
    Column("id_ciudad", Integer, ForeignKey("ciudad.id_ciudad")),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("nombre_gerente", String(255))
)

RegistrarGerenteRegional = Table("registrar_gerente_regional", meta,
    Column("id_gerente_regional", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, ForeignKey("channel.id_channel")),
    Column("id_ciudad", Integer, ForeignKey("ciudad.id_ciudad")),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("nombre_gerente", String(255))
)

RegistrarGerenteCiudad = Table("registrar_gerente_ciudad", meta,
    Column("id_gerente_ciudad", Integer, primary_key=True, autoincrement=True),
    Column("id_ciudad", Integer, ForeignKey("ciudad.id_ciudad")),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("id_channel", Integer, ForeignKey("channel.id_channel")),
    Column("nombre_gerente_ciudad", String(255))
)

RegistrarAdminProyectos = Table("registrar_admin_proyectos", meta,
    Column("id_admin_proyectos", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, ForeignKey("channel.id_channel")),
    Column("id_ciudad", Integer, ForeignKey("ciudad.id_ciudad")),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("nombre_admin_proyectos", String(255))
)


RegistroJefeVentas = Table("registro_jefe_ventas", meta,
    Column("id_jefe_venta", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, ForeignKey("channel.id_channel")),
    Column("id_ciudad", Integer, ForeignKey("ciudad.id_ciudad")),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("id_gerente", Integer, ForeignKey("registrar_gerente.id_gerente"), nullable=True, default=None),
    Column("nombre_jefe", String(255))
)

RegistroAdministrador = Table("registro_administrador", meta,
    Column("id_administrador", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, ForeignKey("channel.id_channel")),
    Column("id_ciudad", Integer, ForeignKey("ciudad.id_ciudad")),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("nombre_administrador", String(255))
)


meta.create_all(db)