FROM python:3.10.4-alpine

WORKDIR /xtrim_edificio

COPY . /xtrim_edificio/

COPY ./requirements.txt /xtrim_edificio/requirements.txt

RUN apk update && apk add --no-cache gcc musl-dev linux-headers

RUN apk add --no-cache --virtual .build-deps gcc musl-dev linux-headers

# RUN apt install -y apparmor apturl && pip install -r requirements.txt

RUN pip install --no-cache-dir --upgrade -r /xtrim_edificio/requirements.txt

RUN ls -la

# ENV user=root password= host=146.190.208.100:3306 database=database

CMD python -m uvicorn index:app --host 0.0.0.0 --port 3003
# CMD [ "uvicorn", "index:app", "--port", "3003" ]