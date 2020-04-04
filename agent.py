#!/usr/bin/env python3
import pika
import sys

class Agent():

    def __init__(self, host = 'localhost', port = 5672, queue_name = 'classroom_queue'):
        self.__host = host
        self.__port = port
        self.__queue = queue_name

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        self.__host = value

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value

    @property
    def queue(self):
        return self.__queue

    @queue.setter
    def queue(self, value):
        self.__queue = value


    def produceFanout(self, message):
        #establish a connection with RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.0.5"))
        channel = connection.channel()

        #define the exchange
        channel.exchange_declare(exchange = 'classroom_logs', exchange_type = 'fanout')

        #send message through the declared exchange and the routing_key (delivery_mode make message persistent)
        props = pika.BasicProperties(headers= {'status': 'Tomando Lista:',"alarm":"LISTA"},type ="RFID Sensor")
        channel.basic_publish(exchange = 'classroom_logs', routing_key = '', body = message, properties = props)

        print("[x] Sent %r \n" %message)

        #finish the connection with RabbitMQ server
        connection.close()

    def getNameFanout(self):
        #establish a connection with RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.0.5"))
        channel = connection.channel()

        #define the exchange
        channel.exchange_declare(exchange = 'classroom_logs', exchange_type = 'fanout')

        #define the classroom_queue to receive the message
        result = channel.queue_declare(queue = '', exclusive = True)
        return result.method.queue, channel#
    def consumeFanout(self, name, channel):
        channel.queue_bind(exchange = 'classroom_logs', queue = name)

        #In this function we make the work with received information
        def callback(ch, method, properties, body):
            print('[x] Received %r' %body)

        #prepare to consume message
        #channel.basic_consume(queue = name, on_message_callback = callback, auto_ack = True)

        #consume a message
        return channel.basic_get(queue = name, auto_ack = True)

    def produceDirect(self, message):
        user = "RaspPi"
        pwd = "Tangente123"
        credentials = pika.PlainCredentials(user, pwd)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.0.20",credentials=credentials))
        channel = connection.channel()

        channel.queue_declare(queue='Doc_Manage',durable=True)

        channel.basic_publish(exchange='', routing_key='Doc_Manage', body=message)
        print(" [x] Sent " + str(message))
        connection.close()

    def consumeDirect(self):
        user = "RaspPi"
        pwd = "Tangente123"
        credentials = pika.PlainCredentials(user, pwd)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.0.20",credentials=credentials))
        channel = connection.channel()

        channel.queue_declare(queue='Doc_Manage',durable=True)


        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)


        channel.basic_consume(
            queue='Doc_Manage', on_message_callback=callback, auto_ack=True)

        return channel.basic_get(queue='Doc_Manage',auto_ack=True)
    def run(self):
        while True:
            opt = input('(1) producer, (2) consumer, (other) quit  -->')
            if ((opt == '1') or (opt == '2')):
                if (opt == '1'):
                    msg = input('\n Enter the message -->')
                    self.produce_message(msg)
                    print('\n message sended!! \n')
                else:
                    self.consumer_message()
            else:
                sys.exit()

if __name__ == "__main__":
    agent1 = Agent(host = '192.168.0.5', port = 5672, queue_name = 'classroom_ToPI')
