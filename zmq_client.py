#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import numpy as np
context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.1.158:5555")

def buf2Array(buff,size):
    dt = np.dtype('float32')
    dt = dt.newbyteorder('<')
    x= np.frombuffer(buff, dt, count=-1, offset=0)
    if (len(x)%1024==0)and(len(x)>1024):
        y=x.reshape(-1,size)
        data_col = y[1,:].tolist()
        print(max(data_col),data_col.index(max(data_col)))
#  Do 10 requests, waiting each time for a response
while True:
    #  Get the reply.
    socket.send(b"Hello")
    buff = socket.recv()
    buf2Array(buff,1024)
    #print("Received reply %s [ %s ]" % (request, message))