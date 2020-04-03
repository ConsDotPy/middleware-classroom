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
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.__host), self.__port, '/')
        channel = connection.channel()

        #define the exchange
        channel.exchange_declare(exchange = 'classroom_logs', exchange_type = 'fanout')

        #send message through the declared exchange and the routing_key (delivery_mode make message persistent)
        props = pika.BasicProperties(headers= {'status': 'Tomando Lista:',"alarm":"LISTA"},type ="RFID Sensor")
        channel.basic_publish(exchange = 'classroom_logs', routing_key = '', body = message, properties = props)

        print("[x] Sent %r \n" %message)

        #finish the connection with RabbitMQ server
        connection.close()

    def consumeFanout(self):
        #establish a connection with RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.__host))
        channel = connection.channel()

        #define the exchange
        channel.exchange_declare(exchange = 'classroom_logs', exchange_type = 'fanout')

        #define the classroom_queue to receive the message
        result = channel.queue_declare(queue = '', exclusive = True) #

        channel.queue_bind(exchange = 'classroom_logs', queue = result.method.queue)

        #In this function we make the work with received information
        def callback(ch, method, properties, body):
            print('[x] Received %r' %body)

        #prepare to consume message
        channel.basic_consume(queue = result.method.queue, on_message_callback = callback, auto_ack = True)

        #consume a message
        print('\n Waiting for messages. To exit press CTRL+C \n')
        channel.start_consuming()

    def produceDirect(self, message):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.0.20"))
        channel = connection.channel()

        channel.queue_declare(queue='Doc_Manage')

        channel.basic_publish(exchange='Orders', routing_key='Felix', body=message)
        print(" [x] Sent " + str(message))
        connection.close()

    def consumeDirect(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="192.168.0.20"))
        channel = connection.channel()

        channel.queue_declare(queue='Doc_Manage')


        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)


        channel.basic_consume(
            queue='Doc_Manage', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
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
