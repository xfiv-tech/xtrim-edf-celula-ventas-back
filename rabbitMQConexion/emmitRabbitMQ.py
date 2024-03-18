import json
import sys

import pika
import threading

from rabbitMQConexion.conexionRabbitMQ import openConection

class EmitRabbitMQNewUser(threading.Thread):
    def __init__(self, body):
        self.body = json.dumps(body).encode('utf-8')
        threading.Thread.__init__(self)
    def run(self):
        routing_key = 'celula.user.new'
        try:
            connection = openConection()
            channel = connection.channel()
            channel.basic_publish(exchange='celula', routing_key=routing_key, body=self.body,
                                  properties=pika.BasicProperties(
                                      delivery_mode = 2, # make message persistent
                                      headers = {'system':'celula_ventas'}
                                  ))
            print("Conectado")
        except Exception as e:
            print("Ocurrio un error al establece conexion con el RabbitMQ")
            print(f"Error: {e}({sys.exc_info()[-1].tb_lineno})")
        finally:
            connection.close()

class EmitRabbitMQEditUser(threading.Thread):
    def __init__(self, body):
        self.body = json.dumps(body).encode('utf-8')
        threading.Thread.__init__(self)

    def run(self):
        routing_key = 'celula.user.edit'
        try:
            connection = openConection()
            channel = connection.channel()
            channel.basic_publish(exchange='celula', routing_key=routing_key, body=self.body,
                                  properties=pika.BasicProperties(
                                      delivery_mode=2,  # make message persistent
                                      headers={'system': 'celula_ventas'}
                                  ))
            print("Conectado")
        except Exception as e:
            print("Ocurrio un error al establece conexion con el RabbitMQ")
            print(f"Error: {e}({sys.exc_info()[-1].tb_lineno})")
        finally:
            connection.close()

#PRUEBA EMITIENDO EVENTO
# emi = EmitRabbitMQNewUser('{body:"body"')
# emi.start()