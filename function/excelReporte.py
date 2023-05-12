from openpyxl import Workbook
from pydantic import BaseModel
from typing import List, Optional
from controller.AdminProyectController import SelectAdminProyectCiudad, SelectGerenteCiudad, SelectGerenteRegional, SelectJefeVenta, SelectLiderPeloton
from function.ftp import ftp_close, ftp_connect, ftp_list, ftp_upload
import os
from dotenv import load_dotenv

load_dotenv()

from model.channel import Channel, Ciudad, Estados, Genero, Modalidad, Operador, RegistrarAdminProyectos, RegistrarGerenteCiudad, RegistrarGerenteRegional, RegistrarVendedor, RegistroJefeVentas, SistemaOperativo 
from database.db import db

HOST = os.getenv("HOST_FTP")
USER = os.getenv("USER_FTP")
PASS = os.getenv("PASS_FTP")

class ReporteExcel(BaseModel):
    id_registrar_vendedor: int
    id_channel: int
    id_ciudad: int
    id_operador: int 
    id_sistema_operativo: int 
    id_estado: int
    id_genero: int
    id_modalidad: int 
    cedula: str 
    telefono: str 
    codigo_vendedor: str 
    usuario_equifax: str 
    nombre_vendedor: str 
    fecha_ingreso: str 
    # id_gerente: int = None
    # nombre_gerente: str  
    id_gerente_regional: int = None 
    nombre_gerente_regional: str 
    id_gerente_ciudad: int = None
    nombre_gerente_ciudad: str 
    id_jefe_venta: int = None
    nombre_jefe_venta: str 
    nombre_admin_proyectos: Optional[str] = None
    # ciudad_gestion: str 
    lider_check: bool = False
    id_lider_peloton: Optional[str] = None
    meta_volumen_internet: Optional[int] = 0
    meta_dolares_internet: Optional[float] = 0.0
    meta_volumen_telefonia: Optional[int] = 0
    meta_dolares_telefonia: Optional[float] = 0.0
    meta_volumen_television: Optional[int] = 0
    meta_dolares_television: Optional[float] = 0.0
    fecha_salida: str = None
    sector_residencia: str 
    email: str 
    dias_inactivo: int 
    channel: str 
    ciudad: str
    region: str 
    estado: str 
    operador: str 
    genero: str 
    modalidad: str 
    sistema_operativo: str


async def get_infoReporte(ciudad: list):
    try:
        data = []
        for i in ciudad:
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
                ]).where(RegistrarVendedor.c.id_ciudad == i["id_ciudad"])         
            res = db.execute(query).fetchall()
            print("res",res)
            for i in res:
                data.append(i)


        dataInfo = []
        for i in data:
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
                "id_lider_peloton": await SelectLiderPeloton(i.id_lider_peloton),
                # "id_gerente": data_gerente.id_gerente,
                # "nombre_gerente": data_gerente.nombre_gerente,
                "id_gerente_regional": i.id_gerente_regional,
                "nombre_gerente_regional": await SelectGerenteRegional(i.id_gerente_regional),
                "id_gerente_ciudad": i.id_gerente_ciudad,
                "nombre_gerente_ciudad": await SelectGerenteCiudad(i.id_gerente_ciudad),
                "id_jefe_venta": i.id_jefe_venta,
                "nombre_jefe_venta": await SelectJefeVenta(i.id_jefe_venta),
                "nombre_admin_proyectos": await SelectAdminProyectCiudad(i.id_ciudad),
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

        return dataInfo
    except Exception as e:
        return {"error": str(e)}
    
async def get_tdd_excel_workbook(ciudad: list, usuario: str): 
    try:
        ftp = ftp_connect(HOST, USER, PASS)
        ftplist = ftp_list(ftp, "QlikView")
        ftplistCelula = ftp_list(ftp, "Celula_Ventas")
        print("ftplist",ftplist)
        print("ftplistCelula",ftplistCelula)
        wb = Workbook() 
        ws = wb.active 
        data = await get_infoReporte(ciudad)

        ws.append([
            "CIUDAD","ESTADO","COD. VENDEDOR","VENDEDOR","LIDER DE PELOTON", "ADMINISTRADOR PROYECTO", "JEFE DE VENTAS","GERENTE CIUDAD", "GERENTE REGIONAL", "CANAL DE VENTA","OPERADOR","SISTEMA OPERATIVO","GENERO","MODALIDAD","FECHA INGRESO","FECHA SALIDA","SECTOR RESIDENCIA","EMAIL","DIAS INACTIVO","CELULAR",
            "META VOLUMEN INTERNET","META DOLARES INTRNET",
            "META VOLUMEN TELEFONIA","META DOLARES TELEFONIA",
            "META VOLUMEN TELEVISION","META DOLARES TELEVISION",
            "USUARIO EQUIFAX","CEDULA",
        ])
        for i in data:
            k = ReporteExcel(**i)
            print(k)
            # k.id_lider_peloton = k.id_lider_peloton if k.id_lider_peloton != 0 else "SIN LIDER"
            ws.append([
                k.ciudad, k.estado, k.codigo_vendedor, k.nombre_vendedor, k.id_lider_peloton, k.nombre_admin_proyectos, k.nombre_jefe_venta, k.nombre_gerente_ciudad, k.nombre_gerente_regional, k.channel, k.operador, k.sistema_operativo, k.genero, k.modalidad, k.fecha_ingreso, k.fecha_salida, k.sector_residencia, k.email, k.dias_inactivo, k.telefono, 
                k.meta_volumen_internet, k.meta_dolares_internet, 
                k.meta_volumen_telefonia, k.meta_dolares_telefonia,
                k.meta_volumen_television, k.meta_dolares_television,
                k.usuario_equifax, k.cedula
            ])

        wb.save(usuario)
        # ftp.upload(usuario, f"/QlikView/{usuario}")
        print(f"STOR /QlikView/Celula_Ventas/{usuario}")
        ftp.storbinary(f"STOR /QlikView/Celula_Ventas/{usuario}", open(usuario, "rb"))
        print(ftp.nlst())
        ftp_close(ftp)
        return {
            "success": True,
        }
    except Exception as e:
        print("get excel",e.args)
        return {
            "error": str(e.args),
            "success": False,
        }
    