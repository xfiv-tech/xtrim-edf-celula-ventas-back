FROM python:3.10.4-alpine

WORKDIR /xtrim_edificio

COPY . /xtrim_edificio/

COPY ./requirements.txt /xtrim_edificio/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /xtrim_edificio/requirements.txt

RUN pip install PyJWT


RUN ls -la

CMD python -m uvicorn index:app --host 0.0.0.0 --port 3003