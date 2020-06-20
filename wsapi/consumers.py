# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import random
import zmq
import numpy as np

class APIConsumer(WebsocketConsumer):
    zmq_context = zmq.Context()
    socket = zmq_context.socket(zmq.REQ)
    def connect(self):
        self.api_name = self.scope['url_route']['kwargs']['api_name']
        self.api_group_name = 'api_%s' % self.api_name
        print(self.api_name)
        print(self.api_group_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.api_group_name,
            self.channel_name
        )
        self.accept()
        try:
            #  Socket to talk to server
            #self.socket.setsockopt(ZMQ_IPV6, True)
            #self.socket.connect("tcp://[240e:311:955:1600:db47:33e8:8608:53ac]:5555")
            self.socket.connect( "tcp://192.168.1.158:5555" )

        except:
            print("An exception occurred")

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.api_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        message = text_data
        #val_rand = -(random.random())*100
        self.socket.send(b"Hello")
        buff = self.socket.recv()
        val_zmq = self.buf2Array(buff,1024)
        #print(message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.api_group_name,
            {
                'type': 'chat_message',
                'data': val_zmq
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['data']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'data': message
        }))

    def buf2Array(self,buff,size):
        dt = np.dtype('float32')
        dt = dt.newbyteorder('<')
        x= np.frombuffer(buff, dt, count=-1, offset=0)
        if (len(x)%1024==0)and(len(x)>1024):
            y=x.reshape(-1,size)
            data_col = y[1,:].tolist()
            return max(data_col)
            #print(max(data_col),data_col.index(max(data_col)))
