import pika
import sys
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv("RABBITMQ_USER")
password = os.getenv("RABBITMQ_PASS")
host = os.getenv("RABBITMQ_HOST")
port = os.getenv("RABBITMQ_PORT")
queue_name = os.getenv("RABBITMQ_QUEUENAME")

credential = pika.PlainCredentials(user, password)

def openConection():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, credentials=credential)
        )
        print("Se establecio conexion con el RabbitMQ")
        return connection
    except Exception as e:
        print("Ocurrio un error al establece conexion con el RabbitMQ")
        print(f"Error: {e}({sys.exc_info()[-1].tb_lineno})")

def closeConection(connection):
    try:
        connection.close()
        print("Se ha cerrado la conexion")
    except Exception as e:
        print("Ocurrio un error al establece conexion con el RabbitMQ")
        print(f"Error: {e}({sys.exc_info()[-1].tb_lineno})")


#PRUEBA DE CONEXION RABBITMQ
#a = openConection()