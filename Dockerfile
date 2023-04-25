FROM python:3.10.4-alpine

RUN pip install --upgrade pip

WORKDIR /xtrim

COPY ./requirements.txt /xtrim/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /xtrim/requirements.txt 
# && 
# \
#     pip install --no-cache-dir --upgrade uvicorn[standard] && \
#     pip install --no-cache-dir --upgrade websockets && \
#     pip install --upgrade pip 

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