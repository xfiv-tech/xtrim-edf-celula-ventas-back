from io import BytesIO
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from database.db import db
from model.edificio import Edicifios
from model.administrador import Administradores

from openpyxl import Workbook 

reporte = APIRouter()



def get_tdd_excel_workbook(): 
    wb = Workbook() 
    ws = wb.active 
    query = Edicifios.join(Administradores).select().with_only_columns([
        Edicifios.c.id,
        Edicifios.c.idAdministrador,
        Administradores.c.nombreAdministrador,
        Administradores.c.email,
        Edicifios.c.id_edificio,
        Edicifios.c.sector,
        Edicifios.c.ciudad,
        Edicifios.c.coordenadas,
        Edicifios.c.ctaReferencia,
        Edicifios.c.nombreEdificio,
        Edicifios.c.referencia,
        Edicifios.c.adjunto,
        Edicifios.c.data_creatd,
        Edicifios.c.data_update,
        ])
    data = db.execute(query).fetchall()
    # print(data)
    ws.append(['id', 'idAdministrador', 'nombreAdministrador', 'email', 'id_edificio', 'sector', 'ciudad', 'coordenadas', 'ctaReferencia', 'nombreEdificio', 'referencia', 'adjunto', 'data_creatd', 'data_update'])
    for row in data:
        print(row.id)
        print(row.id)
        print(row.id)
        print(row.id)
        ws.append([row.id, row.idAdministrador, row.nombreAdministrador, row.email, row.id_edificio, row.sector, row.ciudad, row.coordenadas, row.ctaReferencia, row.nombreEdificio, row.referencia, row.adjunto, row.data_creatd, row.data_update])

    return wb 


@reporte.post("/reporte", tags=["reporte"])
async def get_reporte():
    try:
        wb = get_tdd_excel_workbook() 

        # file_stream = BytesIO() 
        wb.save('reporte.xlsx')
        # file_stream.seek(0 ) 

        return FileResponse(
            path='reporte.xlsx',
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
            filename='reporte.xlsx',
            )
        
        # return {
        #     "code": "0",
        #     "data": data,
        #     "message": "Edificios listados correctamente"
        # }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })


@reporte.post("/reporte", tags=["reporte"])
async def get_reporte_list():
    try:
        query = Edicifios.join(Administradores).select().with_only_columns([
        Edicifios.c.id,
        Edicifios.c.idAdministrador,
        Administradores.c.nombreAdministrador,
        Administradores.c.email,
        Edicifios.c.id_edificio,
        Edicifios.c.sector,
        Edicifios.c.ciudad,
        Edicifios.c.coordenadas,
        Edicifios.c.ctaReferencia,
        Edicifios.c.nombreEdificio,
        Edicifios.c.referencia,
        Edicifios.c.adjunto,
        Edicifios.c.data_creatd,
        Edicifios.c.data_update,
        ])
        data = db.execute(query).fetchall()

        return {
            "code": "0",
            "data": data,
            "message": "listados correctamente"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            "code": "-1",
            "data": str(e)
        })