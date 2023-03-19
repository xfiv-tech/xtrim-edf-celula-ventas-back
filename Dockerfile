FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install core dependencies.
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# WORKDIR /xtrim

# COPY . /xtrim/

# COPY ./requirements.txt /xtrim/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /xtrim/requirements.txt

RUN ls -la

LABEL maintainer="Dario Javier Marret medranda <javier_dario_marret@hotmail.com>" \
      version="1.0" \
      description="Xtrim API Celulas de ventas"
# ENV user=root password=Marret123456+-* host=146.190.208.100:3306 database=database

CMD python -m uvicorn index:app --host 0.0.0.0 --port 3003
# CMD [ "uvicorn", "index:app", "--port", "3003" ]



# Allow statements and log messages to immediately appear in the Knative logs


# Copy local code to the container image.



