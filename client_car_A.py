"""
Send location and action to server:

find_location() - Get current location WORK AS A THREAD.
bypass() - # Detect lanes and return 1 if the car is outside the lane line.
process_server_response() - Get information from the server (other cars) and process.

"""
import socket
import lane_detection
import process as proc
import cv2 as cv
import location
import threading
import time

current_location = '' # global variable


# Get current location and update current_location - WORK AS A THREAD
def find_location():
    print('Get current location',end='')
    global current_location
    while True:
        current_location = location.get_current_location()

# Detect lanes and return 1 if the car outside the lane line
def bypass(cap):

    out_of_lane = lane_detection.detection(cap)  # Is True if the car is out side the lane.

    # If the car is out side the lane send 1 to server
    if out_of_lane:
        send_to_server = '1'
    elif not out_of_lane:
        send_to_server = '0'

    return send_to_server

# Process server response
def process_server_response(server_response):

    if server_response == 'N':
        return
    # Location of other car
    x_coordinate = server_response[0:8]
    y_coordinate = server_response[8:17]

    other_location = (x_coordinate,y_coordinate)
    # Measur distance
    distance = location.measuring_distance(current_location,other_location)
    # Lane of other car
    action = server_response[-1]
    # If there is a car out if his lane in 0.2 miles
    car_out_of_lane = (action == '1') and (distance < 0.2)

    if car_out_of_lane:
        print('WARNING')
    else:
        print('Safe way')


# Get current location and action and create message to server
def create_message(bypass,location):

    x_coordinate, y_coordinate = location
    message = x_coordinate + y_coordinate + bypass
    message = message.encode()
    return message


# Start client
def start():

    test_path = 'Images/Test/testvideo.mp4'  # test path
    test_camara = proc.break_video_to_frames(test_path)

    HOST = '127.0.0.1'
    PORT = 65432
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # Get current location
    location_thread = threading.Thread(target=find_location)
    location_thread.daemon = True
    location_thread.start()


    # Send massage to server
    while True:

        # wait for location
        if current_location is '':
            print('.',end='')
            time.sleep(2)
        else:
            print('\n'+ 'Location is found')
            for frame in range(len(test_camara)):

                # Show the road
                cv.putText(test_camara[frame],'Car A ', (370, 350), cv.FONT_HERSHEY_SIMPLEX, 1,(0, 255, 0),2)
                cv.putText(test_camara[frame],'Car B ', (50, 30), cv.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255),2)

                cv.imshow('Α', test_camara[frame])
                if cv.waitKey(1) & 0xFF == 27:
                    break

                bypass_to_server = bypass(test_camara[frame])# bypass - Is b'1' if the car outside the lane

                # Create massage to server that include if the car is outside the lane, and car location
                message = create_message(bypass_to_server,current_location)

                # Send to server the side of the car
                s.sendall(message)

                # Get action from other cars
                server_response = str(s.recv(17), "utf-8")

                # Process server response
                process_server_response(server_response)


start()