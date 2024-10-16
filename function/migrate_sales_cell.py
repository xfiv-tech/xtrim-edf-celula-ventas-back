import sys
from datetime import datetime

import urllib3
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Float,
    create_engine,
    MetaData,
    select,
    desc,
)
import time
from dotenv import load_dotenv
import json
import os
import requests
from openpyxl import Workbook
import uuid

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()
url = "https://cw.xtrim.com.ec/rest/cw-user-manager-api/v1.0/post/create_user"
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
database = os.getenv("database")
token = os.getenv("TOKEN_MIGRACION_PROD")

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

DATABASE_CONNECTION_URI = f"mysql+pymysql://{user}:{password}@{host}/{database}"
engine = create_engine(DATABASE_CONNECTION_URI, echo=False)
meta = MetaData()
db = engine.connect()
Roles = Table(
    "roles",
    meta,
    Column("id_roles", Integer, primary_key=True, autoincrement=True),
    Column("rol", String(255)),
    Column("descripcion", String(255)),
    Column("data_created", DateTime),
    Column("data_update", DateTime),
)

Ciudad = Table(
    "ciudad",
    meta,
    Column("id_ciudad", Integer, primary_key=True, autoincrement=True),
    Column("ciudad", String(255), unique=True),
    Column("region", String(255)),
)
Estados = Table(
    "estados",
    meta,
    Column("id_estado", Integer, primary_key=True, autoincrement=True),
    Column("estado", String(255), unique=True),
)
Modalidad = Table(
    "modalidad",
    meta,
    Column("id_modalidad", Integer, primary_key=True, autoincrement=True),
    Column("modalidad", String(255), unique=True),
)
Channel = Table(
    "channel",
    meta,
    Column("id_channel", Integer, primary_key=True, autoincrement=True),
    Column("channel", String(255), unique=True),
)
RegistrarGerenteRegional = Table(
    "registrar_gerente_regional",
    meta,
    Column("id_gerente_regional", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, nullable=True),
    Column("id_ciudad", Integer, nullable=True),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("nombre_gerente", String(255)),
    Column("cedula", String(13)),
    Column("telefono", String(255)),
    Column("email", String(255)),
)
RegistrarGerenteCiudad = Table(
    "registrar_gerente_ciudad",
    meta,
    Column("id_gerente_ciudad", Integer, primary_key=True, autoincrement=True),
    Column("id_ciudad", Integer, nullable=True),
    Column("id_channel", Integer, nullable=True),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("nombre_gerente_ciudad", String(255)),
    Column("cedula", String(13)),
    Column("telefono", String(255)),
    Column("email", String(255)),
)
RegistroJefeVentas = Table(
    "registro_jefe_ventas",
    meta,
    Column("id_jefe_venta", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, nullable=True),
    Column("id_ciudad", Integer, nullable=True),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column(
        "id_gerente_ciudad",
        Integer,
        ForeignKey("registrar_gerente_ciudad.id_gerente_ciudad"),
        nullable=True,
        default=None,
    ),
    Column("email", String(255)),
    Column("cedula", String(13)),
    Column("telefono", String(12)),
    Column("nombre_jefe", String(255)),
)
Operador = Table(
    "operador",
    meta,
    Column("id_operador", Integer, primary_key=True, autoincrement=True),
    Column("operador", String(255), unique=True),
)
RegistroAdministrador = Table(
    "registro_administrador",
    meta,
    Column("id_administrador", Integer, primary_key=True, autoincrement=True),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("email", String(255), unique=True),
    Column("password", String(255)),
    Column("perfil", String(255)),
    Column("id_roles", Integer, ForeignKey("roles.id_roles")),
    Column("nombre_administrador", String(255)),
)
RegistrarVendedor = Table(
    "registrar_vendedor",
    meta,
    Column("id_registrar_vendedor", Integer, primary_key=True, autoincrement=True),
    Column("id_channel", Integer, ForeignKey("channel.id_channel")),
    Column("id_ciudad", Integer, ForeignKey("ciudad.id_ciudad")),
    Column("id_operador", Integer, ForeignKey("operador.id_operador")),
    Column(
        "id_sistema_operativo",
        Integer,
        ForeignKey("sistema_operativo.id_sistema_operativo"),
    ),
    Column("id_estado", Integer, ForeignKey("estados.id_estado")),
    Column("id_genero", Integer, ForeignKey("genero.id_genero")),
    Column("id_modalidad", Integer, ForeignKey("modalidad.id_modalidad")),
    Column("codigo_vendedor", String(255), unique=True),
    Column("usuario_equifax", String(255)),
    Column("nombre_vendedor", String(255)),
    Column("fecha_ingreso", String(255)),
    Column(
        "id_gerente_regional",
        Integer,
        ForeignKey("registrar_gerente_regional.id_gerente_regional"),
        nullable=True,
        default=None,
    ),
    Column(
        "id_gerente_ciudad",
        Integer,
        ForeignKey("registrar_gerente_ciudad.id_gerente_ciudad"),
        nullable=True,
        default=None,
    ),
    Column(
        "id_jefe_venta",
        Integer,
        ForeignKey("registro_jefe_ventas.id_jefe_venta"),
        nullable=True,
        default=None,
    ),
    Column("id_lider_peloton", Integer, nullable=True, default=None),
    Column("lider_check", Boolean, default=False),
    Column("meta_volumen_internet", Integer, default=0),
    Column("meta_dolares_internet", Float, default=0.0),
    Column("meta_volumen_telefonia", Integer, default=0),
    Column("meta_dolares_telefonia", Float, default=0.0),
    Column("meta_volumen_television", Integer, default=0),
    Column("meta_dolares_television", Float, default=0.0),
    Column("fecha_salida", String(255), nullable=True),
    Column("sector_residencia", String(255)),
    Column("email", String(255)),
    Column("cedula", String(13)),
    Column("telefono", String(12)),
    Column("campana", String(255)),
    Column("dias_inactivo", Integer, default=0),
)


def migrate_sales_cell():
    wb = Workbook()
    hoja = wb.active
    columna = [
        ("COD_VENDEDOR", "A1"),
        ("REQUEST", "B1"),
        ("RESPONSE", "C1"),
        ("ERROR", "D1"),
    ]
    for col in columna:
        hoja[col[1]] = col[0]
    cod_vendedores = [
        103427391,
        102654513,
        102654466,
        101259274,
        100538028,
        102909426,
        103775570,
        103826377,
        100970883,
        103168890,
        104489812,
        102101113,
        101917042,
        105290051,
        105142329,
        98868411,
        100150425,
        100296303,
        100516981,
        102551810,
        102566682,
        102992839,
        103689274,
        103690556,
        104492409,
        104624796,
        104892422,
        104791679,
        104791657,
        105286653,
    ]
    mail_jefe_ventas = [
        33,  # Teresa leon id_jefe_venta
        48,  # Wilmer montenegro id_jefe_venta
    ]
    mail_gerente_ciudad = []
    mail_gerente_regional = []
    print(f"Hay {len(cod_vendedores)} vendedores")
    print(f"Hay {len(mail_jefe_ventas)} jefe ventas")
    print(f"Hay {len(mail_gerente_ciudad)} gerente ciudad")
    print(f"Hay {len(mail_gerente_regional)} gerente regional")
    query = (
        select(
            RegistrarVendedor.c.id_registrar_vendedor,
            RegistrarVendedor.c.codigo_vendedor,
            RegistrarVendedor.c.nombre_vendedor,
            RegistrarVendedor.c.cedula,
            RegistrarVendedor.c.telefono,
            RegistrarVendedor.c.email,
            RegistrarVendedor.c.id_estado,
            RegistrarVendedor.c.id_ciudad,
            RegistrarVendedor.c.id_channel,
            RegistrarVendedor.c.id_operador,
            RegistrarVendedor.c.id_modalidad,
            RegistrarVendedor.c.usuario_equifax,
            RegistrarVendedor.c.fecha_ingreso,
            RegistrarVendedor.c.fecha_salida,
            RegistrarVendedor.c.sector_residencia,
            RegistrarVendedor.c.id_jefe_venta,
        )
        .where(RegistrarVendedor.c.codigo_vendedor.in_(cod_vendedores))
        .order_by(RegistrarVendedor.c.id_registrar_vendedor)
    )

    init = time.time()
    data = db.execute(query).fetchall()
    v = {}
    count = 0
    print(f"Total vendor encontrados {len(data)}")
    for row in data:
        print(row)
        count += 1
        if row[-1] in v:
            v[row[-1]].append(row[1])
        else:
            v[row[-1]] = [row[1]]
        temp2 = db.execute(
            select(Ciudad.c.ciudad).where(Ciudad.c.id_ciudad == row[7])
        ).fetchall()
        temp3 = db.execute(
            select(Channel.c.channel).where(Channel.c.id_channel == row[8])
        ).fetchall()
        ciudad = temp2[0][0]
        channel = temp3[0][0]
        estado = row[6] != 2
        temp = db.execute(
            select(RegistroJefeVentas.c.cedula).where(
                RegistroJefeVentas.c.id_jefe_venta == row[-1]
            )
        ).fetchall()
        operador = db.execute(
            select(Operador.c.operador).where(Operador.c.id_operador == row[9])
        ).fetchall()[0][0]
        modalidad = db.execute(
            select(Modalidad.c.modalidad).where(Modalidad.c.id_modalidad == row[10])
        ).fetchall()[0][0]
        usuE = row[11]
        fechaS = ""
        if row[12] != "Invalid date":
            fechaS = row[13]
        fechaI = row[12]
        sector = row[14]
        telefono = row[4]
        seller_code = row[1]
        cedula = row[3]
        adicional = temp[0][0]
        email = row[5]
        lastname = ""
        name = row[2]
        rol = "vendedor"
        username = row[1]
        body = (
            f'{{ "channel": "CHANNEL", "data": {{ "enable": {str(estado).lower()}, "attributes": {{"seller_code": "{seller_code}", "boss_sales_manager": "{adicional}", '
            f'"cedula": "{cedula}" , "ciudad": "{ciudad}" , "telefono": "{telefono}" , "channel": "{channel}", "operador": "{operador}", "modalidad": "{modalidad}", '
            f'"usuario_equipax": "{usuE}", "fecha_ingreso": "{fechaI}", "fecha_salida": "{fechaS}", "sector_residencia": "{sector}"}}, "email": "{email}", "last_name": "{lastname}", "name": "{name}", "rol": "{rol}", "user_name": "{username}" }}, "externalTransactionId": "{uuid.uuid4()}" }}'
        )
        try:
            resp = requests.post(
                url, json=json.loads(body), headers=headers, verify=False
            )
            print(resp.content)
            if resp.status_code == 200:
                print(resp.json())
                hoja.append(username, body, str(resp.json()), False)
            else:
                hoja.append(username, body, str(resp.json()), True)
            # hoja.append([username, body, 'Ok',False])
        except Exception as e:
            msg_err = f"Error: {e} ({sys.exc_info()[-1].tb_lineno})"
            hoja.append(username, body, "No se obtuvo alguna respuesta", msg_err)

    query = (
        select(
            RegistroJefeVentas.c.id_jefe_venta,
            RegistroJefeVentas.c.nombre_jefe,
            RegistroJefeVentas.c.id_ciudad,
            RegistroJefeVentas.c.cedula,
            RegistroJefeVentas.c.telefono,
            RegistroJefeVentas.c.email,
            RegistroJefeVentas.c.id_estado,
            RegistroJefeVentas.c.id_channel,
            RegistroJefeVentas.c.id_gerente_ciudad,
        )
        .filter(RegistroJefeVentas.c.id_jefe_venta.in_(mail_jefe_ventas))
        .order_by(RegistroJefeVentas.c.id_jefe_venta)
    )
    data = db.execute(query).fetchall()
    count = 0
    print(f"Total jefe encontrados {len(data)}")
    for row in data:
        count += 1
        temp = db.execute(
            select(RegistrarGerenteCiudad.c.cedula).where(
                RegistrarGerenteCiudad.c.id_gerente_ciudad == row[-1]
            )
        ).fetchall()
        temp2 = db.execute(
            select(Ciudad.c.ciudad).where(Ciudad.c.id_ciudad == row[2])
        ).fetchall()
        temp3 = db.execute(
            select(Channel.c.channel).where(Channel.c.id_channel == row[7])
        ).fetchall()
        if len(temp2) > 0:
            ciudad = temp2[0][0]
        else:
            ciudad = ""
        if len(temp3) > 0:
            channel = temp3[0][0]
        else:
            channel = ""
        cedula = row[3]
        estado = row[6] != 2
        telefono = row[4]
        external_trasn = uuid.uuid4()
        adicional = temp[0][0]
        email = row[5] if row[5] else f"email_fake_{external_trasn}_@gmail.com"
        lastname = ""
        name = row[1]
        rol = "jefe de ventas"
        username = f"jefe_de_ventas_{count}"
        body = (
            f'{{ "channel": "CHANNEL", "data": {{  "enable": {str(estado).lower()}, "attributes":'
            f' {{"city_manager": "{adicional}", "cedula": "{cedula}" , "telefono": "{telefono}"  , "ciudad": "{ciudad}" , "channel": "{channel}"}}, '
            f'"email": "{email}", "last_name": "{lastname}", "name": "{name}", "rol": "{rol}", "user_name": "{username}" }}, '
            f'"externalTransactionId": "{external_trasn}" }}'
        )
        print(body)
        try:
            resp = requests.post(
                url, json=json.loads(body), headers=headers, verify=False
            )
            print(resp.content)
            if resp.status_code == 200:
                print(resp.json())
                hoja.append([username, body, str(resp.json()), False])
            else:
                hoja.append(username, body, str(resp.json()), True)
            # hoja.append([username, body, 'Ok', False])
        except Exception as e:
            msg_err = f"Error: {e} ({sys.exc_info()[-1].tb_lineno})"
            hoja.append(username, body, "No se obtuvo alguna respuesta", msg_err)

    query = (
        select(
            RegistrarGerenteCiudad.c.id_gerente_ciudad,
            RegistrarGerenteCiudad.c.nombre_gerente_ciudad,
            RegistrarGerenteCiudad.c.id_ciudad,
            RegistrarGerenteCiudad.c.cedula,
            RegistrarGerenteCiudad.c.telefono,
            RegistrarGerenteCiudad.c.email,
            RegistrarGerenteCiudad.c.id_estado,
            RegistrarGerenteCiudad.c.id_channel,
        )
        .filter(RegistrarGerenteCiudad.c.email.in_(mail_gerente_ciudad))
        .order_by(RegistrarGerenteCiudad.c.id_gerente_ciudad)
    )
    data = db.execute(query).fetchall()
    c = {}
    count = 0
    print(f"Total g-ciudad encontrados {len(data)}")
    for row in data:
        count += 1
        if row[2] in c:
            c[row[2]].append(row[3])
        else:
            c[row[2]] = [row[3]]
        temp2 = db.execute(
            select(Ciudad.c.ciudad).where(Ciudad.c.id_ciudad == row[2])
        ).fetchall()
        temp3 = db.execute(
            select(Channel.c.channel).where(Channel.c.id_channel == row[7])
        ).fetchall()
        adicional = ""
        if len(temp2) > 0:
            ciudad = temp2[0][0]
        else:
            ciudad = ""
        if len(temp3) > 0:
            channel = temp3[0][0]
        else:
            channel = ""
        cedula = row[3]
        estado = row[6] != 2
        email = row[5]
        telefono = row[4]

        lastname = ""
        name = row[1]
        rol = "gerente_de_ciudad"
        username = row[3]
        body = (
            f'{{ "channel": "CHANNEL", "data": {{ "enable": {str(estado).lower()},"attributes":'
            f' {{"regional_manager": "{adicional}", "cedula": "{cedula}" , "telefono": "{telefono}" , "ciudad": "{ciudad}" , "channel": "{channel}"}}, '
            f'"email": "{email}", "last_name": "{lastname}", "name": "{name}", "rol": "{rol}", "user_name": "{username}" }}, '
            f'"externalTransactionId": "{ uuid.uuid4() }"}}'
        )
        print(body)
        try:
            if username != None:
                resp = requests.post(
                    url, json=json.loads(body), headers=headers, verify=False
                )
                print(resp.content)
                if resp.status_code == 200:
                    print(resp.json())
                    hoja.append(username, body, str(resp.json()), False)
                else:
                    hoja.append(username, body, str(resp.json()), True)
                # hoja.append([username, body, 'Ok', False])
        except Exception as e:
            msg_err = f"Error: {e} ({sys.exc_info()[-1].tb_lineno})"
            hoja.append(username, body, "No se obtuvo alguna respuesta", msg_err)
    query = (
        select(
            RegistrarGerenteRegional.c.id_gerente_regional,
            RegistrarGerenteRegional.c.nombre_gerente,
            RegistrarGerenteRegional.c.id_ciudad,
            RegistrarGerenteRegional.c.cedula,
            RegistrarGerenteRegional.c.telefono,
            RegistrarGerenteRegional.c.email,
            RegistrarGerenteRegional.c.id_estado,
            RegistrarGerenteRegional.c.id_channel,
        )
        .filter(RegistrarGerenteRegional.c.email.in_(mail_gerente_regional))
        .order_by(RegistrarGerenteRegional.c.id_gerente_regional)
    )
    data = db.execute(query).fetchall()
    count = 0
    print(f"Total g-regional encontrados {len(data)}")
    for row in data:
        count += 1
        temp2 = db.execute(
            select(Ciudad.c.ciudad).where(Ciudad.c.id_ciudad == row[2])
        ).fetchall()
        temp3 = db.execute(
            select(Channel.c.channel).where(Channel.c.id_channel == row[7])
        ).fetchall()
        adicional = ""
        if len(temp2) > 0:
            ciudad = temp2[0][0]
        else:
            ciudad = ""
        if len(temp3) > 0:
            channel = temp3[0][0]
        else:
            channel = ""
        cedula = row[3]
        estado = row[6] != 2
        email = row[5]
        telefono = row[4]
        lastname = ""
        name = row[1]
        rol = "gerente_regional"
        username = row[3]
        body = (
            f'{{ "channel": "CHANNEL", "data": {{ "enable": {str(estado).lower()}, "attributes":'
            f' {{"regional_manager": "{adicional}", "cedula": "{cedula}" , "telefono": "{telefono}"  , "ciudad": "{ciudad}" , "channel": "{channel}"}}, '
            f'"email": "{email}", "last_name": "{lastname}", "name": "{name}", "rol": "{rol}", "user_name": "{username}" }}, '
            f'"externalTransactionId": "{uuid.uuid4()}" }}'
        )
        print(body)
        try:
            if username != None:
                resp = requests.post(
                    url, json=json.loads(body), headers=headers, verify=False
                )
                print(resp.content)
                if resp.status_code == 200:
                    print(resp.json())
                    hoja.append(username, body, str(resp.json()), False)
                else:
                    hoja.append(username, body, str(resp.json()), True)
                # hoja.append([username, body, 'Ok', False])
        except Exception as e:
            msg_err = f"Error: {e} ({sys.exc_info()[-1].tb_lineno})"
            hoja.append(username, body, "No se obtuvo alguna respuesta", msg_err)

    fin = time.time()
    print("time ejecucion ", (fin - init))
    date_crr = datetime.now()
    # Obtener la ruta del directorio actual del script
    nombre_directorio = "logs_migracion"
    ruta_actual = os.path.dirname(__file__)

    # Unir la ruta actual con el nombre del directorio
    ruta_directorio_completa = os.path.join(ruta_actual, nombre_directorio)
    if not os.path.exists(ruta_directorio_completa):
        # Si no existe, crearlo
        os.makedirs(ruta_directorio_completa)
        print(
            f"Directorio '{nombre_directorio}' creado satisfactoriamente en {ruta_directorio_completa}"
        )
    else:
        print(
            f"El directorio '{nombre_directorio}' ya existe en {ruta_directorio_completa}"
        )
    wb.save(
        f"{ruta_directorio_completa}/log_migración_{date_crr.year}{date_crr.month}{date_crr.day}{date_crr.hour}{date_crr.minute}{date_crr.second}.xlsx"
    )
    wb.close()
    print(v)


migrate_sales_cell()
