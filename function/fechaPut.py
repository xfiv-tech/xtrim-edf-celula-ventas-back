



import datetime

#Validar fecha actual sea del 1 al 5 de cada mes
async def ValidarFechaActual():
    fecha_actual = datetime.datetime.now()
    dia_actual = fecha_actual.day
    mes_actual = fecha_actual.month
    anio_actual = fecha_actual.year
    if dia_actual >= 1 and dia_actual <= 5:
        return True
    else:
        return False