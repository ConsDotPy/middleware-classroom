import pika
import sys

class Agent():

    def __init__(self, host = '192.168.0.5', port = 5672, queue_name = 'classroom_queue'):        
        self.__host = host
        self.__port = port
        self.__queue = queue_name

        self.run()
    
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
    
    
    def produce_message(self, message):
        #establish a connection with RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.__host))
        channel = connection.channel()

        #create a classroom_queue queue to which the message will be delivered and received
        #channel.queue_declare(queue = self.__queue)

        #define the exchange
        channel.exchange_declare(exchange = 'classroom_logs', exchange_type = 'direct')

        #send message through the declared exchange and the routing_key (delivery_mode make message persistent)
        channel.basic_publish(exchange = 'classroom_logs', routing_key = 'attendance', body = message, properties = pika.BasicProperties(delivery_mode = 2))

        print("[x] Sent %r \n" %message)

        #finish the connection with RabbitMQ server
        connection.close()        
    
    def consumer_message(self):
        #establish a connection with RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.__host))
        channel = connection.channel()

        #define the exchange
        channel.exchange_declare(exchange = 'classroom_logs', exchange_type = 'direct')

        #define the classroom_queue to receive the message
        result = channel.queue_declare(queue = '', exclusive = True, durable = True) #

        channel.queue_bind(exchange = 'classroom_logs', queue = result.method.queue, routing_key = 'attendance')

        #In this function we make the work with received information
        def callback(ch, method, properties, body):
            print('[x] Received %r' %body)

        #prepare to consume message
        channel.basic_consume(queue = result.method.queue, on_message_callback = callback, auto_ack = True)

        #consume a message
        print('\n Waiting for messages. To exit press CTRL+C \n')
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


agent = Agent('127.0.1.1')
