FROM python:3.10.4-alpine

WORKDIR /xtrim

COPY . /xtrim/

COPY ./requirements.txt /xtrim/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /xtrim/requirements.txt

RUN ls -la

# ENV user=root password=Marret123456+-* host=146.190.208.100:3306 database=database

CMD python -m uvicorn index:app --host 0.0.0.0 --port 3003
# CMD [ "uvicorn", "index:app", "--port", "3003" ]