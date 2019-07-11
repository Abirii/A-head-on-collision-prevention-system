'''
data:
Hold connections and address.
add() - Add to data set
remove() - Remove from data set
restart() - Restart data set
get_all_connections() - Get all connections from data set
get_all_address() - Get all address from data set
sent_location_to_all_cars() - Sent location to all cars from current car
'''
from threading import Lock

# Each car update the data set
class Data_Set:
    MIN_DISTANCE = 50

    def __init__(self):
        self.data_set = []
        self.lock = Lock()

    # Add to data set
    def add(self,conn_address):
        with self.lock:
         self.data_set.append(conn_address)

    # Remove from data set
    def remove(self, car_number):
        with self.lock:
            del self.data_set[car_number]

 # Restart data set
    def restart(self):
        # Closing previous connections when server.py file is restarted
        for conn in self.data_set:
            conn[0].close()

        # Delete data set
        del self.data_set[:]

    # Get all connections
    def get_connections(self):
        with self.lock:
            connections = []
            for data in self.data_set:
                connections.append(data[0])

        return connections

    # Get all address
    def get_address(self):
        with self.lock:
            address = []
            for data in self.data_set:
                address.append(data[1])

        return address

    # Sent location to all the cars
    def send_location_to_all(self,this,bypass):
        with self.lock:

            for conn in self.data_set:

                if len(self.data_set) == 1:
                    message = 'N'.encode()
                    conn[0].sendall(message)


                elif this is not conn[0]:
                    message = str(bypass).encode()
                    conn[0].sendall(message)

