import schedule
import time
import datetime
import calendar
from openpyxl import Workbook
from function.excelReporte import ReporteExcel
from database.db import db
from model.channel import asignacion_ciudades_admin_proyectos
from model.channel import Channel, Ciudad, Estados, Genero, Modalidad, Operador, RegistrarAdminProyectos, RegistrarDistribuidor, RegistrarGerenteCiudad, RegistrarGerenteRegional, RegistrarVendedor, RegistroJefeVentas, SistemaOperativo
from function.ftp import ftp_close, ftp_connect, ftp_list
import os
from dotenv import load_dotenv
load_dotenv()

HOST = os.getenv("HOST_FTP")
USER = os.getenv("USER_FTP")
PASS = os.getenv("PASS_FTP")


def SelectLiderPeloton(id_lider_peloton:int, id_channel:int):
    try:
        if id_lider_peloton == None or id_lider_peloton == 0:
            return "NO APLICA"
        
        # sacar el nombre del canal
        if id_channel == None or id_channel == 0:
            return "NO APLICA"
        
        if id_channel == 1 or id_channel == 4 or id_channel == 5:
            nombre_lider = RegistrarDistribuidor.select().where(RegistrarDistribuidor.c.id_registrar_distribuidor == id_lider_peloton)
            query = db.execute(nombre_lider).fetchall()
            for i in query:
                return i["nombre_distribuidor"]
            

        nombre_lider = RegistrarVendedor.select().where(RegistrarVendedor.c.id_registrar_vendedor == id_lider_peloton)
        query = db.execute(nombre_lider).fetchall()
        for i in query:
            return i["nombre_vendedor"]
    except Exception as e:
        print("SelectLiderPeloton",e.args)
        return "NO APLICA"
    
def SelectJefeVenta(id_jefe_venta:int):
    try:
        if id_jefe_venta == None or id_jefe_venta == 0:
            return "SIN JEFE VENTA"
        nombre_jefe = RegistroJefeVentas.select().where(RegistroJefeVentas.c.id_jefe_venta == id_jefe_venta)
        query = db.execute(nombre_jefe).fetchall()
        for i in query:
                return i["nombre_jefe"]
    except Exception as e:
        print(e)
        return "SIN JEFE VENTA"    

def SelectGerenteCiudad(id_gerente_ciudad:int):
    try:
        if id_gerente_ciudad == None or id_gerente_ciudad == 0:
            return "SIN GERENTE CIUDAD"
        nombre_gerente = RegistrarGerenteCiudad.select().where(RegistrarGerenteCiudad.c.id_gerente_ciudad == id_gerente_ciudad)
        query = db.execute(nombre_gerente).fetchall()
        for i in query:
                return i["nombre_gerente_ciudad"]
    except Exception as e:
        print(e)
        return "SIN GERENTE CIUDAD"

def SelectGerenteRegional(id_gerente_regional:int):
    try:
        if id_gerente_regional == None or id_gerente_regional == 0:
            return "SIN GERENTE REGIONAL"
        nombre_gerente = RegistrarGerenteRegional.select().where(RegistrarGerenteRegional.c.id_gerente_regional == id_gerente_regional)
        query = db.execute(nombre_gerente).fetchall()
        for i in query:
                return i["nombre_gerente"]
    except Exception as e:
        print(e)
        return "SIN GERENTE REGIONAL"

def ListarCiudadesAPCiudad(id_admin_proyectos: int):
    try:
        query = asignacion_ciudades_admin_proyectos.join(Ciudad, asignacion_ciudades_admin_proyectos.c.id_ciudad == Ciudad.c.id_ciudad).select().where(
            asignacion_ciudades_admin_proyectos.c.id_admin_proyectos == id_admin_proyectos
        )
        data = db.execute(query).fetchall()
        infoData = []
        for i in data:
            infoData.append({
                "id_asignacion_ciudades_admin_proyectos": i.id_asignacion_ciudades_admin_proyectos,
                "id_ciudad": i.id_ciudad,
                "id_admin_proyectos": i.id_admin_proyectos,
                "ciudad": i.ciudad
            })
        return infoData
    except Exception as e:
        return {"status": 400, "message": str(e)}
    
def SelectAdminProyectCiudad(id_ciudad:int):
    try:
        nombre_admin_proyect = RegistrarAdminProyectos.select()
        admin_proyect = db.execute(nombre_admin_proyect).fetchall()
        infoData = []
        for i in admin_proyect:
            response = ListarCiudadesAPCiudad(i["id_admin_proyectos"])
            if response != None:
                for j in response:
                    if j["id_ciudad"] == id_ciudad:
                        infoData.append({
                            "id_admin_proyectos": i["id_admin_proyectos"],
                            "nombre_admin_proyectos": i["nombre_admin_proyectos"],
                        })
                        return infoData[0]["nombre_admin_proyectos"]

        return infoData[0]["nombre_admin_proyectos"]
    except Exception as e:
        print(e)
        return None

def tarea_programada():
    print("Tarea programada ejecutada a las 12 de la noche.")
    query = RegistrarVendedor.join(Ciudad, RegistrarVendedor.c.id_ciudad == Ciudad.c.id_ciudad).join(
                Estados, RegistrarVendedor.c.id_estado == Estados.c.id_estado).join(
                Channel, RegistrarVendedor.c.id_channel == Channel.c.id_channel).join(
                Operador, RegistrarVendedor.c.id_operador == Operador.c.id_operador).join(
                SistemaOperativo, RegistrarVendedor.c.id_sistema_operativo == SistemaOperativo.c.id_sistema_operativo).join(
                Genero, RegistrarVendedor.c.id_genero == Genero.c.id_genero).join(
                Modalidad, RegistrarVendedor.c.id_modalidad == Modalidad.c.id_modalidad).select().with_only_columns([
                Channel.c.channel,
                Ciudad.c.ciudad,
                Ciudad.c.region,
                Estados.c.estado,
                Operador.c.operador,
                Genero.c.genero,
                Modalidad.c.modalidad,
                RegistrarVendedor.c.id_sistema_operativo,
                SistemaOperativo.c.sistema_operativo,
                RegistrarVendedor.c.id_modalidad,
                RegistrarVendedor.c.id_lider_peloton,
                RegistrarVendedor.c.id_estado,
                RegistrarVendedor.c.id_genero,
                RegistrarVendedor.c.id_ciudad,
                RegistrarVendedor.c.id_registrar_vendedor,
                RegistrarVendedor.c.id_channel,
                RegistrarVendedor.c.id_gerente_regional,
                RegistrarVendedor.c.id_gerente_ciudad,
                RegistrarVendedor.c.id_jefe_venta,
                RegistrarVendedor.c.cedula,
                RegistrarVendedor.c.telefono,
                RegistrarVendedor.c.id_operador,
                RegistrarVendedor.c.codigo_vendedor,
                RegistrarVendedor.c.usuario_equifax,
                RegistrarVendedor.c.nombre_vendedor,
                RegistrarVendedor.c.fecha_ingreso,
                RegistrarVendedor.c.fecha_salida,
                RegistrarVendedor.c.sector_residencia,
                RegistrarVendedor.c.lider_check,
                RegistrarVendedor.c.meta_volumen_internet,
                RegistrarVendedor.c.meta_dolares_internet,
                RegistrarVendedor.c.meta_volumen_telefonia,
                RegistrarVendedor.c.meta_dolares_telefonia,
                RegistrarVendedor.c.meta_volumen_television,
                RegistrarVendedor.c.meta_dolares_television,
                RegistrarVendedor.c.email,
                RegistrarVendedor.c.dias_inactivo
                ])
    res = db.execute(query).fetchall()

    dataInfo = []
    for i in res:
        dataInfo.append({
                "id_registrar_vendedor": i.id_registrar_vendedor,
                "id_channel": i.id_channel,
                "id_ciudad": i.id_ciudad,
                "id_operador": i.id_operador,
                "id_sistema_operativo": i.id_sistema_operativo,
                "id_estado": i.id_estado,
                "id_genero": i.id_genero,
                "id_modalidad": i.id_modalidad,
                "cedula": i.cedula,
                "telefono": i.telefono,
                "codigo_vendedor": i.codigo_vendedor,
                "usuario_equifax": i.usuario_equifax,
                "nombre_vendedor": i.nombre_vendedor,
                "fecha_ingreso": i.fecha_ingreso,
                "id_lider_peloton": SelectLiderPeloton(i.id_lider_peloton, i.id_channel),
                # "id_gerente": data_gerente.id_gerente,
                # "nombre_gerente": data_gerente.nombre_gerente,
                "id_gerente_regional": i.id_gerente_regional,
                "nombre_gerente_regional": SelectGerenteRegional(i.id_gerente_regional),
                "id_gerente_ciudad": i.id_gerente_ciudad,
                "nombre_gerente_ciudad": SelectGerenteCiudad(i.id_gerente_ciudad),
                "id_jefe_venta": i.id_jefe_venta,
                "nombre_jefe_venta": SelectJefeVenta(i.id_jefe_venta),
                "nombre_admin_proyectos": SelectAdminProyectCiudad(i.id_ciudad),
                # "ciudad_gestion": i.ciudad_gestion,
                "lider_check": i.lider_check,
                "meta_volumen_internet": i.meta_volumen_internet,
                "meta_dolares_internet": i.meta_dolares_internet,
                "meta_volumen_telefonia": i.meta_volumen_telefonia,
                "meta_dolares_telefonia": i.meta_dolares_telefonia,
                "meta_volumen_television": i.meta_volumen_television,
                "meta_dolares_television": i.meta_dolares_television,
                "fecha_salida": i.fecha_salida,
                "sector_residencia": i.sector_residencia,
                "email": i.email,
                "dias_inactivo": i.dias_inactivo,
                "channel": i.channel,
                "ciudad": i.ciudad,  
                "region": i.region,
                "estado": i.estado,
                "operador": i.operador,
                "genero": i.genero,
                "modalidad": i.modalidad,
                "sistema_operativo": i.sistema_operativo
        })

    wb = Workbook() 
    ws = wb.active 
    ws.append([
        "CIUDAD","ESTADO","COD. VENDEDOR","VENDEDOR","LIDER DE PELOTON", "ADMINISTRADOR PROYECTO", "JEFE DE VENTAS","GERENTE CIUDAD", "GERENTE REGIONAL", "CANAL DE VENTA","OPERADOR","SISTEMA OPERATIVO","GENERO","MODALIDAD","FECHA INGRESO","FECHA SALIDA","SECTOR RESIDENCIA","EMAIL","DIAS INACTIVO","CELULAR",
        "META VOLUMEN INTERNET","META DOLARES INTRNET",
        "META VOLUMEN TELEFONIA","META DOLARES TELEFONIA",
        "META VOLUMEN TELEVISION","META DOLARES TELEVISION",
        "USUARIO EQUIFAX","CEDULA",
    ])
    for i in dataInfo:
        k = ReporteExcel(**i)
        print(k)
        ws.append([
            k.ciudad, k.estado, k.codigo_vendedor, k.nombre_vendedor, k.id_lider_peloton, k.nombre_admin_proyectos, k.nombre_jefe_venta, k.nombre_gerente_ciudad, k.nombre_gerente_regional, k.channel, k.operador, k.sistema_operativo, k.genero, k.modalidad, k.fecha_ingreso, k.fecha_salida, k.sector_residencia, k.email, k.dias_inactivo, k.telefono, 
            k.meta_volumen_internet, k.meta_dolares_internet, 
            k.meta_volumen_telefonia, k.meta_dolares_telefonia,
            k.meta_volumen_television, k.meta_dolares_television,
            k.usuario_equifax, k.cedula
        ])
    
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    usuario = ""
    today = datetime.date.today()
    last_day_of_month = calendar.monthrange(today.year, today.month)[1]
    if today.day == last_day_of_month:
        print("El día actual es el último día del mes")
        usuario = "Celula_Ventas_" + fecha + ".xlsx"
    else:
        print("El día actual no es el último día del mes")
        usuario = "Celula_Ventas.xlsx"        
    wb.save(usuario)

        
    # ftp = ftp_connect(HOST, USER, PASS)
    # ftplist = ftp_list(ftp, "QlikView")
    # ftplistCelula = ftp_list(ftp, "Celula_Ventas")
    # print("ftplist",ftplist)
    # print("ftplistCelula",ftplistCelula)   
     
    # print(f"STOR /QlikView/Celula_Ventas/{usuario}")
    # ftp.storbinary(f"STOR /QlikView/Celula_Ventas/{usuario}", open(usuario, "rb"))
    # print(ftp.nlst())
    # ftp_close(ftp)
    return True        
    
  


# Define la tarea programada utilizando la sintaxis de `schedule`

# También puedes utilizar otras unidades de tiempo, como `.hours`, `.days`, `.weeks`, etc.



# def tarea_programada_init():
#     print("Tarea programada ejecutada")
#     tarea_programada()

#Define la tarea programada para que se ejecute cada hora
# schedule.every(4).hours.do(tarea_programada_init)
# schedule.every(1).minutes.do(tarea_programada_init)
# schedule.every(1).seconds.do(tarea_programada_init)
# schedule.every(1).days.do(tarea_programada_init) 


# schedule.every().day.at("00:00").do(tarea_programada_init)

# Define la tarea programada para que se ejecute todos los días a las 12 de la noche
# schedule.every().day.at("00:00").do(tarea_programada_init)

# while True:
#     schedule.run_pending()
#     time.sleep(1)






