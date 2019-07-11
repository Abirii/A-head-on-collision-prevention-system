'''
car:
Car() - thread
run() - get current location and share this location with all other cars
'''
from threading import Thread

class Car(Thread):

    def __init__(self,Data_Set,conn_address):
        super().__init__()
        self.data_set = Data_Set
        self.data= conn_address
        self.conn = conn_address[0]
        self.address = conn_address[1]
        # Save connections and address
        self.save_conn_address()

    # Save connections and address
    def save_conn_address(self):
        self.data_set.add(self.data)

    # Get data from car
    def run(self):
        # Speak with car
        with self.conn:
            while True:
                # Get car response, and convert car response
                client_response = str(self.conn.recv(17), "utf-8")
                # Sent location to all the cars
                self.data_set.send_location_to_all(self.conn,client_response)



