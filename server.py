'''
Server:
listen to requests from client (cars).
Make from each request thread object, each tread get current location and share this location with all the other threads
create_socket() - Create a Socket (TCP)
bind_socket() - Binding the     socket and listening for connections
accepting_connections() - Handling connection from multiple clients and create threads
'''

import socket
from path_communication.car import Car
from path_communication.data import Data_Set

HOST = '127.0.0.1'
PORT = 65432

cars = [] # Hold the threads
data_set = Data_Set() # Create data set of locations

# Create a Socket
def create_socket():
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:

        print("Binding the Port: " + str(PORT))
        s.bind((HOST, PORT))
        s.listen()
    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        # Retrying
        bind_socket()


# Handling connection from multiple clients and saving to a list
def accepting_connections():

    # Restart data set
    data_set.restart()
    # Accepting connections going to run as long as the server is going to be running
    while True:
        try:
            conn, address = s.accept()
            # Prevent a timeout of connections
            s.setblocking(True)
            print("Connection has been established :" + str(address))

            # Create new thread
            cars.append(Car(data_set,(conn,address)))
            cars[-1].daemon = True
            cars[-1].start()
        except:
            print("Error accepting connections")


create_socket()
bind_socket()
accepting_connections()