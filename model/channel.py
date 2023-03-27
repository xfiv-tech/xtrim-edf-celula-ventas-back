from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from database.db import meta, db

Ciudad = Table("ciudad", meta,
    Column("id_ciudad", Integer, primary_key=True, autoincrement=True),
    Column("ciudad", String(255), unique=True),
    Column("region", String(255)),
)
Perfiles = Table("perfiles", meta,
    Column("id_perfil", Integer, primary_key=True, autoincrement=True),
    Column("perfil", String(255), unique=True),
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

RegistrarDistribuidor = Table("registrar_distribuidor", meta,
    Column("id_registrar_distribuidor", Integer, primary_key=True, autoincrement=True),
    Column("id_ciudad", Integer, nullable=True),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("nombre_distribuidor", String(255)),
    Column("responsable", String(255)),
    Column("telefono", String(255)),
    Column("email", String(255)),
    Column("fecha_ingreso", String(255)),
    Column("fecha_salida", String(255), nullable=True)
)

RegistrarGerenteRegional = Table("registrar_gerente_regional", meta,
    Column("id_gerente_regional", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, nullable=True),
    Column("id_ciudad", Integer, nullable=True),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("nombre_gerente", String(255))
)

RegistrarGerenteCiudad = Table("registrar_gerente_ciudad", meta,
    Column("id_gerente_ciudad", Integer, primary_key=True, autoincrement=True),
    Column("id_ciudad", Integer,nullable=True),
    Column("id_channel", Integer, nullable=True),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("nombre_gerente_ciudad", String(255))
)

RegistrarAdminProyectos = Table("registrar_admin_proyectos", meta,
    Column("id_admin_proyectos", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, nullable=True),
    Column("id_ciudad", Integer, nullable=True),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("nombre_admin_proyectos", String(255))
)

RegistroJefeVentas = Table("registro_jefe_ventas", meta,
    Column("id_jefe_venta", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, nullable=True),
    Column("id_ciudad", Integer, nullable=True),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("id_gerente_ciudad", Integer, ForeignKey("registrar_gerente_ciudad.id_gerente_ciudad"), nullable=True, default=None),
    Column("nombre_jefe", String(255))
)

#tabla administrador de sistema
RegistroAdministrador = Table("registro_administrador", meta,
    Column("id_administrador", Integer, primary_key=True, autoincrement=True),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("email", String(255), unique=True),
    Column("password", String(255)),
    Column("id_roles", Integer, ForeignKey("roles.id_roles")),
    Column("nombre_administrador", String(255)),
    Column("perfil", String(255)),
)

# #registro de gerente regional
RegistrarVendedor = Table("registrar_vendedor", meta,
    Column("id_registrar_vendedor", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, ForeignKey("channel.id_channel")),
    Column("id_ciudad", Integer, ForeignKey("ciudad.id_ciudad")),
    Column("id_operador", Integer, ForeignKey("operador.id_operador")),
    Column("id_sistema_operativo", Integer, ForeignKey("sistema_operativo.id_sistema_operativo")),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("id_genero", Integer, ForeignKey("genero.id_genero")),
    Column("id_modalidad", Integer, ForeignKey("modalidad.id_modalidad")),
    Column("codigo_vendedor", String(255), unique=True),
    Column("usuario_equifax", String(255)),
    Column("nombre_vendedor", String(255)),
    Column("fecha_ingreso", String(255)),
    Column("id_gerente_regional", Integer, ForeignKey("registrar_gerente_regional.id_gerente_regional"), nullable=True, default=None),
    Column("id_gerente_ciudad", Integer, ForeignKey("registrar_gerente_ciudad.id_gerente_ciudad"), nullable=True, default=None),
    Column("id_jefe_venta", Integer, ForeignKey("registro_jefe_ventas.id_jefe_venta"), nullable=True, default=None),
    Column("id_lider_peloton", Integer, nullable=True, default=None),
    Column("lider_check", Boolean, default=False),
    Column("meta_volumen", Integer, default=0),
    Column("meta_dolares", Float, default=0.0),
    Column("fecha_salida", String(255), nullable=True),
    Column("sector_residencia", String(255)),
    Column("email", String(255)),
    Column("cedula", String(13)),
    Column("telefono", String(12)),
    Column("dias_inactivo", Integer, default=0),
)

# # Tablas de asignacion de gerentes a ciudades y canales
asignacion_ciudades_gerente_regional = Table("asignacion_ciudades_gerente_regional", meta,
    Column("id_asignacion_ciudades", Integer, primary_key=True, autoincrement=True),
    Column("id_ciudad", Integer, ForeignKey("ciudad.id_ciudad")),
    Column("id_gerente_regional", Integer, ForeignKey("registrar_gerente_regional.id_gerente_regional"))
)

asiganacion_canal_gerente_regional = Table("asignacion_canal_gerente_regional", meta,
    Column("id_asignacion_canal", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, ForeignKey("channel.id_channel")),
    Column("id_gerente_regional", Integer, ForeignKey("registrar_gerente_regional.id_gerente_regional"))
)

asignacion_ciudades_gerente_ciudad = Table("asignacion_ciudades_gerente_ciudad", meta,
    Column("id_asignacion_ciudades_gerente_ciudad", Integer, primary_key=True, autoincrement=True),
    Column("id_ciudad", Integer, ForeignKey("ciudad.id_ciudad")),
    Column("id_gerente_ciudad", Integer, ForeignKey("registrar_gerente_ciudad.id_gerente_ciudad"))
)

asignacion_canal_gerente_ciudad = Table("asignacion_canal_gerente_ciudad", meta,
    Column("id_asignacion_canal_gerente_ciudad", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, ForeignKey("channel.id_channel")),
    Column("id_gerente_ciudad", Integer, ForeignKey("registrar_gerente_ciudad.id_gerente_ciudad"))
)

asignacion_ciudades_jefe_ventas = Table("asignacion_ciudades_jefe_ventas", meta,
    Column("id_asignacion_ciudades_jefe_ventas", Integer, primary_key=True, autoincrement=True),
    Column("id_ciudad", Integer, ForeignKey("ciudad.id_ciudad")),
    Column("id_jefe_venta", Integer, ForeignKey("registro_jefe_ventas.id_jefe_venta"))
)

asignacion_canal_jefe_ventas = Table("asignacion_canal_jefe_ventas", meta,
    Column("id_asignacion_canal_jefe_ventas", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, ForeignKey("channel.id_channel")),
    Column("id_jefe_venta", Integer, ForeignKey("registro_jefe_ventas.id_jefe_venta"))
)

asignacion_ciudades_admin_proyectos = Table("asignacion_ciudades_admin_proyectos", meta,
    Column("id_asignacion_ciudades_admin_proyectos", Integer, primary_key=True, autoincrement=True),
    Column("id_ciudad", Integer, ForeignKey("ciudad.id_ciudad")),
    Column("id_admin_proyectos", Integer, ForeignKey("registrar_admin_proyectos.id_admin_proyectos"))
)

asignacion_canal_admin_proyectos = Table("asignacion_canal_admin_proyectos", meta,
    Column("id_asignacion_canal_admin_proyectos", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, ForeignKey("channel.id_channel")),
    Column("id_admin_proyectos", Integer, ForeignKey("registrar_admin_proyectos.id_admin_proyectos"))
)

asignacion_ciudades_admin = Table("asignacion_ciudades_admin", meta,
    Column("id_asignacion_ciudades_admin", Integer, primary_key=True, autoincrement=True),
    Column("id_ciudad", Integer, ForeignKey("ciudad.id_ciudad")),
    Column("id_administrador", Integer, ForeignKey("registro_administrador.id_administrador"))
)

asignacion_canal_admin = Table("asignacion_canal_admin", meta,
    Column("id_asignacion_canal_admin", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, ForeignKey("channel.id_channel")),
    Column("id_administrador", Integer, ForeignKey("registro_administrador.id_administrador"))
)

asignacion_ciudades_distribuidor = Table("asignacion_ciudades_distribuidor", meta,
    Column("id_asignacion_ciudades_distribuidor", Integer, primary_key=True, autoincrement=True),
    Column("id_ciudad", Integer, ForeignKey("ciudad.id_ciudad")),
    Column("id_registrar_distribuidor", Integer, ForeignKey("registrar_distribuidor.id_registrar_distribuidor"))
)

asignacion_canal_distribuidor = Table("asignacion_canal_distribuidor", meta,
    Column("id_asignacion_canal_distribuidor", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, ForeignKey("channel.id_channel")),
    Column("id_registrar_distribuidor", Integer, ForeignKey("registrar_distribuidor.id_registrar_distribuidor"))
)

meta.create_all(db)