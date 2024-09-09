# Primera etapa para construir las dependencias
FROM python:3.10-slim-bookworm as builder

WORKDIR /xtrim

COPY requirements.txt /xtrim/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt


# Segunda etapa para la imagen final
FROM python:3.10-slim-bookworm

ENV PYTHONUNBUFFERED True


RUN pip install --upgrade pip

ENV APP_HOME /xtrim
WORKDIR $APP_HOME


COPY . /xtrim/

ENV TZ 'America/Guayaquil' 

RUN cd /usr/share/zoneinfo && \ 
    cp -f /usr/share/zoneinfo/$TZ /etc/localtime && \ 
    echo $TZ > /etc/timezone

RUN ls -la

LABEL maintainer="Dario Javier Marret medranda <javier_dario_marret@hotmail.com>" \
      version="1.0" \
      description="Xtrim API Celulas de ventas"

CMD python -m uvicorn index:app --host 0.0.0.0 --port 3003