FROM python:3.10-slim

ENV PYTHONUNBUFFERED True


RUN pip install --upgrade pip

# instalar la version openssl 2.0.0
# RUN apt-get update && apt-get install -y openssl

# instalar la version libssl-dev 2.0.0

# RUN apt-get update && apt-get install -y libssl-dev

ENV APP_HOME /xtrim
WORKDIR $APP_HOME

# RUN apt-get update && apt-get install -y libpq-dev build-essential

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

LABEL maintainer="Geampiere Virgilio Jaramillo Maldonado <geampiere.jaramillo@gmail.com>" \
      version="1.0" \
      description="Xtrim API Celulas de ventas"

CMD python -m uvicorn index:app --host 0.0.0.0 --port 3003