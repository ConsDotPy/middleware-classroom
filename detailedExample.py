#!/usr/bin/env python3
import pika

node = "192.168.0.20"
user = "RaspPi"
pwd = "Tangente123"

# Connect to a remote AMQP server with a username/password
credentials = pika.PlainCredentials(user, pwd)
connection = pika.BlockingConnection(pika.ConnectionParameters(node,
        5672, '/', credentials))                                    
channel = connection.channel()

# Create a queue if it doesn't already exist
channel.queue_declare(queue='Rasp_1',durable=True)

# Define the properties and publish a message
props = pika.BasicProperties(
    headers= {'status': 'Good Quality',"alarm":"LISTA"},
    type ="RFID Sensor")
channel.basic_publish(exchange='Classroom log',
   			routing_key='Rasp_1',body='123123123123 Adrian Constante', 
			properties = props)

connection.close()
