FROM python:3.10.4-alpine

WORKDIR /xtrim

COPY . /xtrim/

COPY ./requirements.txt /xtrim/requirements.txt

RUN pip install  /xtrim/requirements.txt

RUN ls -la

LABEL maintainer="Dario Javier Marret medranda <javier_dario_marret@hotmail.com>" \
      version="1.0" \
      description="Xtrim API Celulas de ventas"

CMD python -m uvicorn index:app --host 0.0.0.0 --port 3003